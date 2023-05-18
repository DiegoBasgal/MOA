# Usina:

"""
    - TDA_NivelMaisCasasAntes
    - SA_RA_PM_810_Tensao_AB
    - SA_RA_PM_810_Tensao_BC
    - SA_RA_PM_810_Tensao_CA
    - SA_RA_PM_810_Potencia_Ativa
"""

# Conector de Campo

"""
    - SA_CD_ResetGeral
    - UG_CD_ResetGeral
    - SA_TDA_ResetGeral

    - SA_CD_Cala_Sirene
    - UG_CD_Cala_Sirene

    -TDA_CD_Hab_Nivel
    -TDA_CD_Desab_Nivel
    -TDA_CD_Hab_Religamento52L
    -TDA_CD_Desab_Religamento52L

    -SA_RD_DJ1_FalhaInt
    -SA_ED_DisjDJ1_Local
    -SA_ED_DisjDJ1_AlPressBaixa
    -SA_ED_DisjDJ1_BloqPressBaixa
    -SA_ED_DisjDJ1_SuperBobAbert2
    -SA_ED_DisjDJ1_Sup125VccBoFeAb1
    -SA_ED_DisjDJ1_Super125VccCiMot
    -SA_ED_DisjDJ1_Super125VccCiCom
    -SA_ED_DisjDJ1_Sup125VccBoFeAb2



"""


# Unidade de Geração:

"""
    - SA_ED_QCAP_Disj52A1Fechado

    # Inforamções UG -> __init__
    - UG{self.id}_RA_PM_710_Potencia_Ativa
    - UG{self.id}_RD_EtapaAux_Sim
    - UG{self.id}_RD_EtapaAlvo_Sim
    - UG{self.id}_RA_Horimetro_Gerador
    - UG{self.id}_RA_Horimetro_Gerador_min

    # Comando de Partida
    - UG{self.id}_CD_ResetGeral
    - UG{self.id}_CD_ResetRele700G
    - UG{self.id}_CD_ResetReleBloq86H
    - UG{self.id}_CD_ResetReleBloq86M
    - UG{self.id}_CD_ResetReleRT
    - UG{self.id}_CD_ResetRV
    - UG{self.id}_CD_Cala_Sirene
    - UG{self.id}_CD_IniciaPartida

    # Comando de Parada
    - UG{self.id}_CD_AbortaPartida
    - UG{self.id}_CD_AbortaSincronismo
    - UG{self.id}_CD_IniciaParada

    # Enviar Setpoint
    - UG{self.id}_CD_RV_RefRemHabilita
    - UG{self.id}_SD_SPPotAtiva

    # Acionar Trip Lógico
    - UG{self.id}_CD_EmergenciaViaSuper

    # Remover Trip Lógico
    - UG{self.id}_ED_ReleBloqA86HAtuado
    - UG{self.id}_RD_700G_Trip

    ## -> Outros comandos utilizam os mesmos registradores

"""

# CONDICIONADORES -> Revisar em campo após os testes