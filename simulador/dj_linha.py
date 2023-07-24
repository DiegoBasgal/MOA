import logging

from temporizador import Temporizador

from dicionarios.const import *

logger = logging.getLogger('__main__')

class Dj52L:
    def __init__(self, shared_dict: "dict", time_handler: "Temporizador") -> None:
        self.dict = shared_dict

        self.segundos_por_passo = time_handler.segundos_por_passo

        self.mola = 0
        self.tempo_carregamento_mola = 2

        self.avisou_trip = False

    def passo(self) -> None:
        self.verificar_inconsistente()

        self.verificar_mola()
        self.verificar_tensao()
        self.verificar_condicao()

        if self.dict['DJ']['debug_dj52L_fechar'] and self.dict['DJ']['debug_dj52L_abrir']:
            self.dict['DJ']['dj52L_aberto'] = True
            self.dict['DJ']['dj52L_fechado'] = True
            self.dict['DJ']['debug_dj52L_abrir'] = False
            self.dict['DJ']['debug_dj52L_fechar'] = False
            self.tripar()

        elif self.dict['DJ']['debug_dj52L_fechar']:
            self.dict['DJ']['debug_dj52L_fechar'] = False
            self.fechar()

        elif self.dict['DJ']['debug_dj52L_abrir']:
            self.dict['DJ']['debug_dj52L_abrir'] = False
            self.abrir()

        if self.dict['DJ']['debug_dj52L_reconhece_reset']:
            self.reconhece_reset()

    def abrir(self) -> None:
        logger.info('[DJ] Abrir.')
        if self.dict['DJ']['dj52L_mola_carregada']:
            self.dict['DJ']['dj52L_aberto'] = True
            self.dict['DJ']['dj52L_fechado'] = False
        else:
            self.tripar('Mandou antes de carregar a mola')

        self.dict['DJ']['dj52L_mola_carregada'] = False

    def fechar(self) -> None:
        if self.dict['DJ']['dj52L_trip']:
            self.dict['DJ']['dj52L_falha_fechamento'] = True
            logger.warning('[DJ] Picou!')
        else:
            if not self.dict['DJ']['dj52L_fechado']:
                logger.info('[DJ] Fechar.')
                if self.dict['DJ']['dj52L_condicao_de_fechamento']:
                    self.dict['DJ']['dj52L_aberto'] = False
                    self.dict['DJ']['dj52L_fechado'] = True
                    self.dict['DJ']['dj52L_mola_carregada'] = False
                else:
                    self.dict['DJ']['dj52L_falha_fechamento'] = True
                    self.tripar('Mandou antes de ter a condição de fechamento')

    def tripar(self, desc=None) -> None:
        if not self.avisou_trip:
            self.avisou_trip = True
            self.dict['DJ']['dj52L_trip'] = True
            self.dict['DJ']['dj52L_aberto'] = True
            self.dict['DJ']['dj52L_fechado'] = False
            self.dict['DJ']['dj52L_mola_carregada'] = False
            self.dict['DJ']['dj52L_falha_fechamento'] = True
            logger.warning('[DJ] Trip!.')

    def reconhece_reset(self) -> None:
        logger.info('[DJ] Reconhece Reset.')
        self.dict['DJ']['dj52L_trip'] = False
        self.dict['DJ']['dj52L_aberto'] = False
        self.dict['DJ']['dj52L_fechado'] = True
        self.dict['DJ']['dj52L_inconsistente'] = False
        self.dict['DJ']['dj52L_falha_fechamento'] = False
        self.dict['DJ']['debug_dj52L_abrir'] = False
        self.dict['DJ']['debug_dj52L_fechar'] = False
        self.dict['DJ']['debug_dj52L_reconhece_reset'] = False
        self.avisou_trip = False

    def verificar_inconsistente(self) -> None:
        if self.dict['DJ']['dj52L_aberto'] == self.dict['DJ']['dj52L_fechado']:
            self.dict['DJ']['dj52L_inconsistente'] = True

    def verificar_mola(self) -> None:
        if not self.dict['DJ']['dj52L_mola_carregada']:
            self.mola += self.segundos_por_passo
            if self.mola >= self.tempo_carregamento_mola:
                self.mola = 0
                self.dict['DJ']['dj52L_mola_carregada'] = True

    def verificar_tensao(self) -> None:
        if not (USINA_TENSAO_MINIMA < self.dict['USN']['tensao_na_linha'] < USINA_TENSAO_MAXIMA):
            self.dict['DJ']['dj52L_falta_vcc'] = True
            self.tripar('Tensão fora dos limites')
        else:
            self.dict['DJ']['dj52L_falta_vcc'] = False

    def verificar_condicao(self) -> None:
        if self.dict['DJ']['dj52L_trip'] \
        or self.dict['DJ']['dj52L_fechado'] \
        or self.dict['DJ']['dj52L_falta_vcc'] \
        or self.dict['DJ']['dj52L_inconsistente'] \
        or not self.dict['DJ']['dj52L_aberto'] \
        or not self.dict['DJ']['dj52L_mola_carregada']:
            self.dict['DJ']['dj52L_condicao_de_fechamento'] = False
        else:
            self.dict['DJ']['dj52L_condicao_de_fechamento'] = True