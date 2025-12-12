"""
Interface de linha de comando (CLI) do validador.
"""

import argparse
import logging
import sys
from pathlib import Path
from datetime import datetime
from typing import List
from concurrent.futures import ProcessPoolExecutor, as_completed

from tqdm import tqdm

from .config import Config
from .parser import NFeParser
from .calculator import IBSCBSCalculator
from .comparator import IBSCBSComparator
from .report import ExcelReportGenerator
from .models import ErrorRecord, ComparisonResult
from .utils import setup_logger

logger = logging.getLogger(__name__)


class NFeValidator:
    """Orquestrador principal do validador."""
    
    def __init__(self, config: Config):
        """
        Inicializa validador.
        
        Args:
            config: Configuração do sistema
        """
        self.config = config
        self.parser = NFeParser(config)
        self.calculator = IBSCBSCalculator(config)
        self.comparator = IBSCBSComparator(config)
        
        self.results: List[ComparisonResult] = []
        self.errors: List[ErrorRecord] = []
    
    def run(self):
        """Executa o processo completo de validação."""
        logger.info("=" * 80)
        logger.info("NF-e IBS/CBS Validator")
        logger.info("=" * 80)
        
        # Criar diretórios de saída
        output_dir = Path(self.config.output_dir)
        output_dir.mkdir(parents=True, exist_ok=True)
        
        # Buscar arquivos XML
        xml_files = self._find_xml_files()
        
        if not xml_files:
            logger.error(f"Nenhum arquivo XML encontrado em: {self.config.input_dir}")
            return
        
        logger.info(f"Encontrados {len(xml_files)} arquivos XML")
        
        # Limitar arquivos se configurado
        if self.config.execution.max_files:
            xml_files = xml_files[:self.config.execution.max_files]
            logger.info(f"Processando apenas {len(xml_files)} arquivos (limite configurado)")
        
        # Processar arquivos
        if self.config.execution.workers > 1:
            logger.info(f"Processamento paralelo com {self.config.execution.workers} workers")
            self._process_parallel(xml_files)
        else:
            logger.info("Processamento sequencial")
            self._process_sequential(xml_files)
        
        # Gerar relatório
        self._generate_report(output_dir)
        
        # Resumo final
        self._print_summary()
    
    def _find_xml_files(self) -> List[Path]:
        """
        Busca arquivos XML no diretório de entrada.
        
        Returns:
            Lista de caminhos de arquivos XML
        """
        input_path = Path(self.config.input_dir)
        
        if not input_path.exists():
            logger.error(f"Diretório de entrada não encontrado: {input_path}")
            return []
        
        if self.config.execution.recurse_subfolders:
            xml_files = list(input_path.rglob("*.xml"))
        else:
            xml_files = list(input_path.glob("*.xml"))
        
        return sorted(xml_files)
    
    def _process_sequential(self, xml_files: List[Path]):
        """
        Processa arquivos XML sequencialmente.
        
        Args:
            xml_files: Lista de arquivos para processar
        """
        for xml_file in tqdm(xml_files, desc="Processando XMLs", unit="arquivo"):
            self._process_file(xml_file)
    
    def _process_parallel(self, xml_files: List[Path]):
        """
        Processa arquivos XML em paralelo.
        
        Args:
            xml_files: Lista de arquivos para processar
        """
        with ProcessPoolExecutor(max_workers=self.config.execution.workers) as executor:
            # Submeter tarefas
            futures = {
                executor.submit(process_single_file, str(xml_file), self.config): xml_file
                for xml_file in xml_files
            }
            
            # Processar resultados com barra de progresso
            for future in tqdm(
                as_completed(futures),
                total=len(futures),
                desc="Processando XMLs",
                unit="arquivo"
            ):
                xml_file = futures[future]
                try:
                    result, error = future.result()
                    
                    if result:
                        self.results.append(result)
                    if error:
                        self.errors.append(error)
                        
                except Exception as e:
                    logger.error(f"Erro ao processar {xml_file.name}: {e}")
                    self.errors.append(ErrorRecord(
                        arquivo=xml_file.name,
                        error_type="ProcessingError",
                        error_message=str(e),
                    ))
    
    def _process_file(self, xml_file: Path):
        """
        Processa um arquivo XML individual.
        
        Args:
            xml_file: Caminho do arquivo
        """
        try:
            # Parse
            nfe = self.parser.parse_file(xml_file)
            
            if nfe is None:
                self.errors.append(ErrorRecord(
                    arquivo=xml_file.name,
                    error_type="ParsingError",
                    error_message="Falha ao fazer parse do XML",
                ))
                return
            
            # Calcular
            self.calculator.calculate_nfe(nfe)
            
            # Comparar
            result = self.comparator.compare_nfe(nfe)
            
            self.results.append(result)
            
        except Exception as e:
            logger.error(f"Erro ao processar {xml_file.name}: {e}", exc_info=self.config.execution.debug)
            self.errors.append(ErrorRecord(
                arquivo=xml_file.name,
                error_type="ProcessingError",
                error_message=str(e),
            ))
    
    def _generate_report(self, output_dir: Path):
        """
        Gera relatório Excel.
        
        Args:
            output_dir: Diretório de saída
        """
        if not self.results and not self.errors:
            logger.warning("Nenhum resultado para gerar relatório")
            return
        
        # Nome do arquivo com timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        report_path = output_dir / f"relatorio_ibs_cbs_{timestamp}.xlsx"
        
        # Resumo da configuração
        config_summary = {
            "Diretório Entrada": self.config.input_dir,
            "Tolerância Absoluta": self.config.tolerance.absolute,
            "Tolerância Percentual (%)": self.config.tolerance.percentage,
            "Fórmula": self.calculator.get_formula_description(),
            "Data Processamento": datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
            "Total XMLs Processados": len(self.results),
            "Total Erros": len(self.errors),
        }
        
        # Gerar relatório
        generator = ExcelReportGenerator(report_path)
        generator.generate(self.results, self.errors, config_summary)
        
        logger.info(f"\nRelatório gerado: {report_path}")
    
    def _print_summary(self):
        """Imprime resumo final no console."""
        logger.info("\n" + "=" * 80)
        logger.info("RESUMO DO PROCESSAMENTO")
        logger.info("=" * 80)
        
        total_nfes = len(self.results)
        total_erros = len(self.errors)
        
        logger.info(f"Total de NF-es processadas: {total_nfes}")
        logger.info(f"Total de erros: {total_erros}")
        
        if total_nfes > 0:
            divergentes = sum(1 for r in self.results if r.status_geral.value == "DIVERGENTE")
            ok = sum(1 for r in self.results if r.status_geral.value == "OK")
            sem_tag = sum(1 for r in self.results if r.status_geral.value == "SEM_TAG")
            
            logger.info(f"\nStatus das NF-es:")
            logger.info(f"  - OK: {ok}")
            logger.info(f"  - Divergentes: {divergentes}")
            logger.info(f"  - Sem Tag IBS/CBS: {sem_tag}")
            
            total_itens = sum(r.total_itens for r in self.results)
            total_diverg_ibs = sum(r.count_divergencias_ibs for r in self.results)
            total_diverg_cbs = sum(r.count_divergencias_cbs for r in self.results)
            
            logger.info(f"\nItens:")
            logger.info(f"  - Total: {total_itens}")
            logger.info(f"  - Divergências IBS: {total_diverg_ibs}")
            logger.info(f"  - Divergências CBS: {total_diverg_cbs}")
        
        logger.info("=" * 80)


def process_single_file(xml_path_str: str, config: Config) -> tuple:
    """
    Função auxiliar para processar arquivo em paralelo.
    
    Args:
        xml_path_str: Caminho do arquivo (string)
        config: Configuração
    
    Returns:
        Tupla (ComparisonResult, ErrorRecord)
    """
    xml_path = Path(xml_path_str)
    
    try:
        parser = NFeParser(config)
        calculator = IBSCBSCalculator(config)
        comparator = IBSCBSComparator(config)
        
        nfe = parser.parse_file(xml_path)
        
        if nfe is None:
            return None, ErrorRecord(
                arquivo=xml_path.name,
                error_type="ParsingError",
                error_message="Falha ao fazer parse do XML",
            )
        
        calculator.calculate_nfe(nfe)
        result = comparator.compare_nfe(nfe)
        
        return result, None
        
    except Exception as e:
        return None, ErrorRecord(
            arquivo=xml_path.name,
            error_type="ProcessingError",
            error_message=str(e),
        )


def main():
    """Função principal do CLI."""
    parser = argparse.ArgumentParser(
        description="Validador de NF-e para IBS/CBS (Reforma Tributária)",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Exemplos de uso:
  python -m nfe_validator --config config.yaml
  python -m nfe_validator --input ./xmls --output ./relatorios
  python -m nfe_validator --input ./xmls --workers 4 --debug
        """
    )
    
    parser.add_argument(
        "--config",
        type=str,
        help="Arquivo de configuração YAML"
    )
    
    parser.add_argument(
        "--input",
        type=str,
        help="Diretório de entrada com XMLs (sobrescreve config)"
    )
    
    parser.add_argument(
        "--output",
        type=str,
        help="Diretório de saída para relatório (sobrescreve config)"
    )
    
    parser.add_argument(
        "--tol-abs",
        type=float,
        help="Tolerância absoluta (sobrescreve config)"
    )
    
    parser.add_argument(
        "--tol-pct",
        type=float,
        help="Tolerância percentual (sobrescreve config)"
    )
    
    parser.add_argument(
        "--workers",
        type=int,
        help="Número de workers para processamento paralelo (sobrescreve config)"
    )
    
    parser.add_argument(
        "--max-files",
        type=int,
        help="Limite de arquivos a processar (sobrescreve config)"
    )
    
    parser.add_argument(
        "--debug",
        action="store_true",
        help="Ativa modo debug"
    )
    
    parser.add_argument(
        "--no-recurse",
        action="store_true",
        help="Não buscar em subpastas"
    )
    
    args = parser.parse_args()
    
    # Carregar configuração
    if args.config:
        config = Config.from_yaml(args.config)
    else:
        config = Config()
    
    # Sobrescrever com argumentos CLI
    if args.input:
        config.input_dir = args.input
    if args.output:
        config.output_dir = args.output
    if args.tol_abs is not None:
        config.tolerance.absolute = args.tol_abs
    if args.tol_pct is not None:
        config.tolerance.percentage = args.tol_pct
    if args.workers is not None:
        config.execution.workers = args.workers
    if args.max_files is not None:
        config.execution.max_files = args.max_files
    if args.debug:
        config.execution.debug = True
    if args.no_recurse:
        config.execution.recurse_subfolders = False
    
    # Configurar logger
    log_level = logging.DEBUG if config.execution.debug else logging.INFO
    output_dir = Path(config.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    log_file = output_dir / f"validador_{timestamp}.log"
    
    setup_logger("nfe_validator", level=log_level, log_file=str(log_file))
    setup_logger(__name__, level=log_level, log_file=str(log_file))
    
    # Executar validador
    try:
        validator = NFeValidator(config)
        validator.run()
        sys.exit(0)
    except KeyboardInterrupt:
        logger.warning("\nProcessamento interrompido pelo usuário")
        sys.exit(1)
    except Exception as e:
        logger.error(f"Erro fatal: {e}", exc_info=True)
        sys.exit(1)


if __name__ == "__main__":
    main()
