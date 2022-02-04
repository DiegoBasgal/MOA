"""
modbus_com.py

Este arquivo contem os endereçõs referentes a usina de COVÓ e funções auxiliares a comunicação via modbus com a usina.

ATENÇÃO, os endereços estão como escritos no ELIPSE E3, deve-se subtrair 1 para utilização do pyModbusTCP

Ex.:
REG_XYZ = 12345
ABC.write_single_register(REG_XYZ-1, 1)

"""

"""

NA CLP ESTA COMO AT%MW???? ou AT%MX????
ENDERECO PARA O PYTHON => 12288 + ????

CLP UG1 DUMP
=======================================================================================================================
=======================================================================================================================
VAR_GLOBAL

	(*	======				Comandos				=======	*)

	MODBUS_Comandos													AT%MW0: ARRAY [00..99] OF WORD;

	MODBUS_Operacao_ResetAlarmes										AT%MX0.0:BOOL;		(*ok*)
	MODBUS_Operacao_ReconheceAlarmes								AT%MX1.0:BOOL;		(*ok*)

	MODBUS_Operacao_UP													AT%MX2.0:BOOL;		(*ok*)
	MODBUS_Operacao_UPGM												AT%MX3.0:BOOL;		(*ok*)
	MODBUS_Operacao_UMD												AT%MX4.0:BOOL;		(*ok*)
	MODBUS_Operacao_UPS												AT%MX5.0:BOOL;		(*ok*)
	MODBUS_Operacao_US													AT%MX6.0:BOOL;		(*ok*)

	MODBUS_Operacao_EmergenciaLigar									AT%MX7.0:BOOL;		(*ok*)
	MODBUS_Operacao_EmergenciaDesligar								AT%MX8.0:BOOL;		(*ok*)

	MODBUS_Turb_ByPassAbrir												AT%MX9.0:BOOL;		(*ok*)
	MODBUS_Turb_ByPassFechar											AT%MX10.0:BOOL;	(*ok*)
	MODBUS_Turb_BorboletaAbrir											AT%MX11.0:BOOL;	(*ok*)
	MODBUS_Turb_BorboletaFechar										AT%MX12.0:BOOL;	(*ok*)
	MODBUS_Turb_FrenagemAplicar										AT%MX13.0:BOOL;
	MODBUS_Turb_FrenagemDesaplicar									AT%MX14.0:BOOL;	(*ok*)
	MODBUS_Turb_FrenagemManual										AT%MX15.0:BOOL;	(*ok*)
	MODBUS_Turb_FrenagemAuto											AT%MX16.0:BOOL;
	MODBUS_Turb_SensorAtivar											AT%MX17.0:BOOL;
	MODBUS_Turb_SensorDesativar										AT%MX18.0:BOOL;

	MODBUS_RegV_Partir													AT%MX19.0:BOOL;	(*ok*)
	MODBUS_RegV_Parar													AT%MX20.0:BOOL;	(*ok*)
	MODBUS_RegV_ColocarCarga											AT%MX21.0:BOOL;	(*ok*)
	MODBUS_RegV_RetirarCarga											AT%MX22.0:BOOL;	(*ok*)
	MODBUS_RegV_IncrementaVelocidade									AT%MX23.0:BOOL;	(*ok*)
	MODBUS_RegV_DecrementaVelocidade								AT%MX24.0:BOOL;	(*ok*)
	MODBUS_RegV_SelecionaModoEstatismo								AT%MX25.0:BOOL;
	MODBUS_RegV_SelecionaModoBaseCarga							AT%MX26.0:BOOL;

	MODBUS_RegT_Ligar													AT%MX27.0:BOOL;	(*ok*)
	MODBUS_RegT_Desligar												AT%MX28.0:BOOL;	(*ok*)
	MODBUS_RegT_IncrementaTensao										AT%MX29.0:BOOL;	(*ok*)
	MODBUS_RegT_DecrementaTensao									AT%MX30.0:BOOL;	(*ok*)
	MODBUS_RegT_PreExcitacao											AT%MX31.0:BOOL;

	MODBUS_Sinc_Ligar														AT%MX32.0:BOOL;
	MODBUS_Sinc_Desligar													AT%MX33.0:BOOL;
	MODBUS_Sinc_ModoAutoLigar											AT%MX34.0:BOOL;	(*ok*)
	MODBUS_Sinc_ModoManualLigar										AT%MX35.0:BOOL;	(*ok*)
	MODBUS_Sinc_ModoBMortaLigar										AT%MX36.0:BOOL;

	MODBUS_Disj52G_Abrir													AT%MX37.0:BOOL;	(*ok*)

	MODBUS_CtrlReativo_ModoFPLigar										AT%MX38.0:BOOL;	(*ok*)
	MODBUS_CtrlReativo_ModoFPDesligar									AT%MX39.0:BOOL;
	MODBUS_CtrlReativo_ModoVArLigar									AT%MX40.0:BOOL;	(*ok*)
	MODBUS_CtrlReativo_ModoVArDesligar								AT%MX41.0:BOOL;

	MODBUS_CtrlPotencia_ModoPotenciaLigar								AT%MX42.0:BOOL;	(*ok*)
	MODBUS_CtrlPotencia_ModoPotenciaDesligar							AT%MX43.0:BOOL;	(*ok*)
	MODBUS_CtrlPotencia_ModoNivelLigar									AT%MX44.0:BOOL;	(*ok*)
	MODBUS_CtrlPotencia_ModoNivelDesligar								AT%MX45.0:BOOL;	(*ok*)
	MODBUS_CtrlPotencia_ReligamentoAutomaticoLigar					AT%MX46.0:BOOL;	(*ok*)
	MODBUS_CtrlPotencia_ReligamentoAutomaticoDesligar				AT%MX47.0:BOOL;	(*ok*)

	MODBUS_UHCT_Bomba01Ligar										AT%MX48.0:BOOL;	(*ok*)
	MODBUS_UHCT_Bomba01Desligar									AT%MX49.0:BOOL;	(*ok*)
	MODBUS_UHCT_Bomba01Principal									AT%MX50.0:BOOL;	(*ok*)
	MODBUS_UHCT_Bomba02Ligar										AT%MX51.0:BOOL;	(*ok*)
	MODBUS_UHCT_Bomba02Desligar									AT%MX52.0:BOOL;	(*ok*)
	MODBUS_UHCT_Bomba02Principal									AT%MX53.0:BOOL;	(*ok*)
	MODBUS_UHCT_BombaAguaLigar										AT%MX54.0:BOOL;
	MODBUS_UHCT_BombaAguaDesligar									AT%MX55.0:BOOL;
	MODBUS_UHCT_SensorAtivar											AT%MX56.0:BOOL;
	MODBUS_UHCT_SensorDesativar										AT%MX57.0:BOOL;
	MODBUS_UHCT_RodizioModoAutomatico								AT%MX58.0:BOOL;	(*ok*)
	MODBUS_UHCT_RodizioModoManual									AT%MX59.0:BOOL;	(*ok*)

	MODBUS_UHLM_Bomba01Ligar										AT%MX60.0:BOOL;	(*ok*)
	MODBUS_UHLM_Bomba01Desligar									AT%MX61.0:BOOL;	(*ok*)
	MODBUS_UHLM_Bomba01Principal									AT%MX62.0:BOOL;
	MODBUS_UHLM_Bomba02Ligar										AT%MX63.0:BOOL;
	MODBUS_UHLM_Bomba02Desligar									AT%MX64.0:BOOL;
	MODBUS_UHLM_Bomba02Principal									AT%MX65.0:BOOL;
	MODBUS_UHLM_JackingLigar											AT%MX66.0:BOOL;
	MODBUS_UHLM_JackingDesligar										AT%MX67.0:BOOL;
	MODBUS_UHLM_ValvulaMecanicaLigar									AT%MX68.0:BOOL;
	MODBUS_UHLM_ValvulaMecanicaDesligar								AT%MX69.0:BOOL;
	MODBUS_UHLM_RodizioModoAutomatico								AT%MX70.0:BOOL;
	MODBUS_UHLM_RodizioModoManual									AT%MX71.0:BOOL;

	MODBUS_OperacaoParada_Reset										AT%MX72.0:BOOL;	(*ok*)


		(* --> Comandos para salvar e restaurar parâmetros da área de memória retentiva <-- *)

	SaveRetainValues														AT%MX100.0: BOOL;
	RestoreRetainValues														AT%MX101.0: BOOL;

END_VAR

VAR_GLOBAL

		(* -=====    Leituras    =====- *)

		VersaoBase													AT%MW475: INT;
		VersaoCustom												AT%MW476: INT;

		NivelJusante													AT%MW477: UINT;
		NivelBarragem												AT%MW478: UINT;(*Nivel Montante Grade*)
		NivelCanal													AT%MW479: UINT;(*Nivel Jusante Grade*)
		NivelCamaraCarga											AT%MW480: UINT;

		Operacao_PainelResetAlarmes								AT%MX481.0: BOOL; (*ok*)
		Operacao_PainelReconheceAlarmes						AT%MX482.0: BOOL; (*ok*)

		Operacao_Info												AT%MW483: INT;
			Operacao_Emergencia									AT%MX483.0: BOOL;(*ok*)
			Operacao_SireneLigada									AT%MX483.1: BOOL;
			Operacao_ModoLocal									AT%MX483.2: BOOL;(*ok*)

			Operacao_SalvandoParametros							AT%MX483.6: BOOL; (*ok*)
			Operacao_RestaurandoParametros						AT%MX483.7: BOOL; (*ok*)

		Operacao_Mensagem										AT%MB967: BYTE;  (*ok*)

		Operacao_EtapaAlvo											AT%MW484: INT; (*ok*)
			Operacao_EtapaAlvoUP									AT%MX484.0: BOOL;
			Operacao_EtapaAlvoUPGM								AT%MX484.1: BOOL;
			Operacao_EtapaAlvoUMD								AT%MX484.2: BOOL;
			Operacao_EtapaAlvoUPS								AT%MX484.3: BOOL;
			Operacao_EtapaAlvoUS									AT%MX484.4: BOOL;

		Operacao_EtapaAtual										AT%MW485: INT; (*ok*)
			Operacao_EtapaAtualUP									AT%MX485.0: BOOL;
			Operacao_EtapaAtualUPGM								AT%MX485.1: BOOL;
			Operacao_EtapaAtualUMD								AT%MX485.2: BOOL;
			Operacao_EtapaAtualUPS								AT%MX485.3: BOOL;
			Operacao_EtapaAtualUS									AT%MX485.4: BOOL; 

		Operacao_EtapaTransicao									AT%MW486: INT; (*ok*)
			Operacao_UPtoUPGM									AT%MX486.0: BOOL; 
			Operacao_UPGMtoUMD									AT%MX486.1: BOOL; 
			Operacao_UMDtoUPS									AT%MX486.2: BOOL; 
			Operacao_UPStoUS										AT%MX486.3: BOOL; 
			Operacao_UStoUPS										AT%MX486.4: BOOL;
			Operacao_UPStoUMD									AT%MX486.5: BOOL; 
			Operacao_UMDtoUPGM									AT%MX486.6: BOOL; 
			Operacao_UPGMtoUP									AT%MX486.7: BOOL; 

		Operacao_InfoParada										AT%MW487: INT; (*ok*)
			Operacao_ParadaNormal								AT%MX487.0: BOOL; 
			Operacao_ParadaEmergencia							AT%MX487.1: BOOL; 
			Operacao_ParadaTRIPAgua								AT%MX487.2: BOOL; 
			Operacao_ParadaTRIPMecanico						AT%MX487.3: BOOL; 
			Operacao_ParadaTRIPEletrico							AT%MX487.4: BOOL; 
			Operacao_ParadaTRIPHidraulico						AT%MX487.5: BOOL; 
			Operacao_ReligamentoAutomatico						AT%MX487.6: BOOL;
			Operacao_PartidaManual								AT%MX487.7: BOOL;
			Operacao_ParadaInfoValida								AT%MX487.15: BOOL;

		UHCT_Info													AT%MW488: INT;
			UHCT_Operacional										AT%MX488.0: BOOL; (*ok*)
			UHCT_Ligada												AT%MX488.1: BOOL;  (*ok*)
			UHCT_SensorDesativado								AT%MX488.2: BOOL;
			UHCT_ModoLocal										AT%MX488.3: BOOL;

		UHCT_Bombas												AT%MW489: INT;
			UHCT_Bomba01											AT%MX489.0: BOOL; (*ok*)
			UHCT_Bomba02											AT%MX489.1: BOOL; (*ok*)

		UHCT_Rodizio												AT%MW490: INT;
			UHCT_Rodizio_Habilitado								AT%MX490.0: BOOL; (*ok*)
			UHCT_RodizioBomba01									AT%MX490.1: BOOL; (*ok*)
			UHCT_RodizioBomba02									AT%MX490.2: BOOL; (*ok*)


		UHCT_Valvulas												AT%MW491: INT;
			UHCT_Valvula01											AT%MX491.0: BOOL; (* Válvula de Reposição *)
			UHCT_Valvula02											AT%MX491.1: BOOL; (* Válvula de Segurança *)
			UHCT_Valvula03											AT%MX491.2: BOOL; (* Válvula Proporcional (Distribuidor) *)
			UHCT_Valvula04											AT%MX491.3: BOOL;

		UHCT_Filtros													AT%MW492: INT;
			UHCT_Filtro01											AT%MX492.0: BOOL; (*ok*)
			UHCT_Filtro02											AT%MX492.1: BOOL; (*ok*)
			UHCT_Filtro03											AT%MX492.2: BOOL;
			UHCT_Filtro04											AT%MX492.3: BOOL;
			UHCT_Filtro05											AT%MX492.4: BOOL;
			UHCT_Filtro06											AT%MX492.5: BOOL;

		UHCT_Pressostatos											AT%MW493: INT;
			UHCT_Pressostato01									AT%MX493.0: BOOL;(* Pressostato Crítica *)
			UHCT_Pressostato02									AT%MX493.1: BOOL;
			UHCT_Pressostato03									AT%MX493.2: BOOL;

		UHCT_NivelOleo_Info										AT%MW494: INT;
			UHCT_NivelOleoLL										AT%MX494.0: BOOL;(*ok*)
			UHCT_NivelOleoL										AT%MX494.1: BOOL;(*ok*)
			UHCT_NivelOleoH										AT%MX494.2: BOOL;
			UHCT_NivelOleoHH										AT%MX494.3: BOOL;

		UHCT_PressaoOleo											AT%MW495: INT; (*ok*)

		UHCT_HorimetroLider										AT%MW496: INT; (*ok*)
		UHCT_HorimetroRetaguarda								AT%MW497: INT; (*ok*)

		UHLM_Info													AT%MW498: INT;
			UHLM_Operacional										AT%MX498.0: BOOL; (*ok*)
			UHLM_Ligada												AT%MX498.1: BOOL; (*ok*)
			UHLM_ModoLocal										AT%MX498.2: BOOL;
			UHLM_ValvulaBombaMecanica							AT%MX498.3: BOOL; (*ok*)
			UHLM_ValvulaSuccao									AT%MX498.4: BOOL; (*ok*)
			UHLM_ResistenciaAquecimento							AT%MX498.5: BOOL; (*ok*)

		UHLM_Bombas												AT%MW499: INT;
			UHLM_Bomba01											AT%MX499.0: BOOL; (*ok*)
			UHLM_Bomba02											AT%MX499.1: BOOL;
			UHLM_Bomba03											AT%MX499.2: BOOL;
			UHLM_Bomba04											AT%MX499.3: BOOL;

		UHLM_Rodizio												AT%MW500: INT;
			UHLM_Rodizio_Habilitado								AT%MX500.0: BOOL;
			UHLM_RodizioBomba01									AT%MX500.1: BOOL;
			UHLM_RodizioBomba02									AT%MX500.2: BOOL;

		UHLM_Filtros													AT%MW501: INT;
			UHLM_Filtro01											AT%MX501.0: BOOL; (*ok*)
			UHLM_Filtro02											AT%MX501.1: BOOL;
			UHLM_Filtro03											AT%MX501.2: BOOL;
			UHLM_Filtro04											AT%MX501.3: BOOL;

		UHLM_Pressostatos											AT%MW502: INT;
			UHLM_Pressostato01									AT%MX502.0: BOOL; (*PressostatoBombaEletrica*)
			UHLM_Pressostato02									AT%MX502.1: BOOL; (*PressostatoBombaMecanica*)
			UHLM_Pressostato03									AT%MX502.2: BOOL;
			UHLM_Pressostato04									AT%MX502.3: BOOL;

		UHLM_Fluxostatos											AT%MW503: INT;
			UHLM_Fluxostato01										AT%MX503.0: BOOL; (*FluxoOleoMancalRadialGuia01*)
			UHLM_Fluxostato02										AT%MX503.1: BOOL; (*FluxoOleoMancalRadialGuia02*)
			UHLM_Fluxostato03										AT%MX503.2: BOOL; (*FluxoOleoMancalAxialEscora*)
			UHLM_Fluxostato04										AT%MX503.3: BOOL; (*FluxoOleoMancalAxialContraEscora*)
			UHLM_Fluxostato05										AT%MX503.4: BOOL; (*FluxoAguaResfriamento*)
			UHLM_Fluxostato06										AT%MX503.5: BOOL;
			UHLM_Fluxostato07										AT%MX503.6: BOOL;
			UHLM_Fluxostato08										AT%MX503.7: BOOL;

		UHLM_NivelOleo_Info										AT%MW504: INT;
			UHLM_NivelOleoLL										AT%MX504.0: BOOL; (*ok*)
			UHLM_NivelOleoL										AT%MX504.1: BOOL;
			UHLM_NivelOleoH										AT%MX504.2: BOOL;
			UHLM_NivelOleoHH										AT%MX504.3: BOOL;

		UHLM_HorimetroLider										AT%MW505: INT;
		UHLM_HorimetroRetaguarda								AT%MW506: INT;

		Turb_Info														AT%MW507: INT;
			Turb_Equalizada											AT%MX507.0: BOOL;  (*ok*)
			Turb_Pronta												AT%MX507.1: BOOL;  (*ok*)
			Turb_Fechada											AT%MX507.2: BOOL;  (*ok*)
			Turb_Travada												AT%MX507.3: BOOL;
			Turb_Parada												AT%MX507.4: BOOL; (*ok*)
			Turb_Equalizando										AT%MX507.5: BOOL;  (*ok*)
			Turb_Fechando											AT%MX507.6: BOOL; (*ok*)
			Turb_SensorDesativado									AT%MX507.7: BOOL;
			Turb_PasDesalinhadas									AT%MX507.8: BOOL;
			Turb_DistribuidorFechado								AT%MX507.9: BOOL; (*ok*)
			Turb_PressostatoVedacaoEixo							AT%MX507.10: BOOL;
			Turb_FluxostatoVedacaoEixo								AT%MX507.11: BOOL;
			Turb_ValvAeracao_Aberta								AT%MX507.12: BOOL;
			Turb_ValvAeracao_Fechada								AT%MX507.13: BOOL;

		Turb_ValvulaByPass											AT%MW508: INT;
			Turb_ByPassAcionamento								AT%MX508.0: BOOL; (*ok*)
			Turb_ByPassFechado									AT%MX508.1: BOOL; (*ok*)
			Turb_ByPassAberto										AT%MX508.2: BOOL; (*ok*)

		Turb_ValvulaBorboleta										AT%MW509: INT;
			Turb_BorboletaAcionamento								AT%MX509.0: BOOL; (*ok*)
			Turb_BorboletaFechada									AT%MX509.1: BOOL;  (*ok*)
			Turb_BorboletaAberta									AT%MX509.2: BOOL;  (*ok*)
			Turb_BorboletaDeriva									AT%MX509.3: BOOL;
			Turb_BorboletaTravada									AT%MX509.4: BOOL; (*ok*)
			Turb_BorboletaMantem									AT%MX509.5: BOOL; (*ok*)

		Turb_TempoCrackEfetivo										AT%MW510: INT;
		Turb_TempoEqualizacaoEfetivo								AT%MW511: INT; (*ok*)

		Turb_PressaoConduto										AT%MW512: INT; (*ok*)
		Turb_PressaoCaixaEspiral									AT%MW513: INT; (*ok*)

		Turb_VazaoTurbinada										AT%MW514: INT;

		Turb_Vibracao01												AT%MW515: INT; (*Vibracao Mancal LA*)
		Turb_Vibracao02												AT%MW516: INT; (*Vibracao Mancal LNA*)
		Turb_Vibracao03												AT%MW517: INT;
		Turb_Vibracao04												AT%MW518: INT;

		Turb_Frenagem												AT%MW519: INT;
			Turb_Frenagem_FreioAplicado							AT%MX519.0: BOOL; (*ok*)
			Turb_Frenagem_FreioManual							AT%MX519.1: BOOL;

		RegV_Info														AT%MW520: INT;
			RegV_Habilitacao											AT%MX520.0: BOOL;  (*ok*)
			RegV_BasedeCarga										AT%MX520.1: BOOL;  (*ok*)
			RegV_RPM030											AT%MX520.2: BOOL;  (*ok*)
			RegV_RPM090											AT%MX520.3: BOOL; (*ok*)
			RegV_CargaZerada										AT%MX520.4: BOOL;  (*ok*)
			RegV_HabilitadoModoEstatismo							AT%MX520.5: BOOL;
			RegV_HabilitadoModoBaseCarga						AT%MX520.6: BOOL;
			RegV_Carga												AT%MX520.7: BOOL;

		RegV_Estado													AT%MW521: INT;
			RegV_Falha												AT%MX521.0: BOOL;
			RegV_Parado												AT%MX521.1: BOOL;
			RegV_ControleManualDistribuidor						AT%MX521.2: BOOL;
			RegV_ControleManualValvula							AT%MX521.3: BOOL;
			RegV_ControleVelocidade								AT%MX521.4: BOOL;
			RegV_CompensacaoPotenciaAtiva						AT%MX521.5: BOOL;
			RegV_ControlePotenciaAtiva								AT%MX521.6: BOOL;

		RegV_Velocidade												AT%MW522: INT;  (*ok*)
		RegV_Distribuidor											AT%MW523: INT;  (*ok*)
		RegV_Rotor													AT%MW524: INT;
		RegV_PotenciaAlvo											AT%MW525: INT;  (*ok*)

		RegT_Info														AT%MW526: INT;
			RegT_Habilitacao											AT%MX526.0: BOOL; (*ok*)
			RegT_TensaoEstabilizada								AT%MX526.1: BOOL; (*ok*)
			RegT_ContatorCampoAberto							AT%MX526.2: BOOL; (*ok*)
			RegT_ContatorCampoFechado							AT%MX526.3: BOOL; (*ok*)
			RegT_PreExcitacaoStatus								AT%MX526.4: BOOL; (*ok*)

		RegT_UExcitacao												AT%MW527: INT;  (*ok*)
		RegT_IExcitacao												AT%MW528: INT;  (*ok*)

		Sinc_Info														AT%MW529: INT;
			Sinc_Habilitacao											AT%MX529.0: BOOL;
			Sinc_ModoAutomatico									AT%MX529.1: BOOL;  (*ok*)
			Sinc_ModoManual										AT%MX529.2: BOOL; (*ok*)
			Sinc_ModoBarraMorta									AT%MX529.3: BOOL;

		Sinc_FrequenciaGerador										AT%MW530: INT; (*ok*)
		Sinc_FrequenciaBarra										AT%MW531: INT; (*ok*)
		Sinc_TensaoGerador											AT%MW532: INT; (*ok*)
		Sinc_TensaoBarra											AT%MW533: INT; (*ok*)

		Disj52G_Info													AT%MW534: INT;
			Disj52G_Aberto											AT%MX534.0: BOOL;  (*ok*)
			Disj52G_Fechado										AT%MX534.1: BOOL;  (*ok*)
			Disj52G_Inconsistente									AT%MX534.2: BOOL;
			Disj52G_TRIP												AT%MX534.3: BOOL;
			Disj52G_Teste											AT%MX534.4: BOOL; (*ok*)
			Disj52G_Inserido											AT%MX534.5: BOOL; (*ok*)
			Disj52G_Extraivel											AT%MX534.6: BOOL;
			Disj52G_MolaCarregada									AT%MX534.7: BOOL; (*ok*)
			Disj52G_CondicaoFechamento							AT%MX534.8: BOOL; 
			Disj52G_FaltaVcc											AT%MX534.9: BOOL;  (*ok*)
			Disj52G_Abriu											AT%MX534.10: BOOL; (*ok*)
			Disj52G_Fechou											AT%MX534.11: BOOL; (*ok*)

		Gerador_TensaoRN											AT%MW535: INT;  (*ok*)
		Gerador_TensaoSN											AT%MW536: INT;  (*ok*)
		Gerador_TensaoTN											AT%MW537: INT;  (*ok*)
		Gerador_TensaoRS											AT%MW538: INT;  (*ok*)
		Gerador_TensaoST											AT%MW539: INT;  (*ok*)
		Gerador_TensaoTR											AT%MW540: INT;  (*ok*)
		Gerador_CorrenteR											AT%MW541: INT;  (*ok*)
		Gerador_CorrenteS											AT%MW542: INT;  (*ok*)
		Gerador_CorrenteT											AT%MW543: INT;  (*ok*)
		Gerador_CorrenteMedia										AT%MW544: INT;  (*ok*)
		Gerador_PotenciaAtiva1										AT%MW545: INT;  (*ok*)
		Gerador_PotenciaAtiva2										AT%MW546: INT;  (*ok*)
		Gerador_PotenciaAtiva3										AT%MW547: INT;  (*ok*)
		Gerador_PotenciaAtivaMedia									AT%MW548: INT;  (*ok*)
		Gerador_PotenciaReativa1									AT%MW549: INT;  (*ok*)
		Gerador_PotenciaReativa2									AT%MW550: INT;  (*ok*)
		Gerador_PotenciaReativa3									AT%MW551: INT;  (*ok*)
		Gerador_PotenciaReativaMedia								AT%MW552: INT;  (*ok*)
		Gerador_PotenciaAparente1									AT%MW553: INT;  (*ok*)
		Gerador_PotenciaAparente2									AT%MW554: INT;  (*ok*)
		Gerador_PotenciaAparente3									AT%MW555: INT;  (*ok*)
		Gerador_PotenciaAparenteMedia							AT%MW556: INT; (*ok*)
		Gerador_FatorPotencia1										AT%MW557: INT;  (*ok*)
		Gerador_FatorPotencia2										AT%MW558: INT;  (*ok*)
		Gerador_FatorPotencia3										AT%MW559: INT;  (*ok*)
		Gerador_FatorPotenciaMedia								AT%MW560: INT;  (*ok*)
		Gerador_Frequencia											AT%MW561: INT;  (*ok*)

		Gerador_EnergiaFornecidaTWh								AT%MW562: INT; (*ok*)
		Gerador_EnergiaFornecidaGWh								AT%MW563: INT; (*ok*)
		Gerador_EnergiaFornecidaMWh								AT%MW564: INT;  (*ok*)
		Gerador_EnergiaFornecidakWh								AT%MW565: INT;  (*ok*)

		Gerador_EnergiaFornecidaTVArh							AT%MW566: INT;  (*ok*)
		Gerador_EnergiaFornecidaGVArh							AT%MW567: INT;  (*ok*)
		Gerador_EnergiaFornecidaMVArh							AT%MW568: INT;  (*ok*)
		Gerador_EnergiaFornecidakVArh							AT%MW569: INT;  (*ok*)

		Gerador_EnergiaConsumidaTVArh							AT%MW570: INT;  (*ok*)
		Gerador_EnergiaConsumidaGVArh							AT%MW571: INT;  (*ok*)
		Gerador_EnergiaConsumidaMVArh							AT%MW572: INT;  (*ok*)
		Gerador_EnergiaConsumidakVArh							AT%MW573: INT;  (*ok*)

		Gerador_FPInfo												AT%MW574: INT;
			Gerador_Fase1Ind										AT%MX574.0: BOOL;  (*ok*)
			Gerador_Fase1Cap										AT%MX574.1: BOOL;  (*ok*)
			Gerador_Fase2Ind										AT%MX574.2: BOOL;  (*ok*)
			Gerador_Fase2Cap										AT%MX574.3: BOOL;  (*ok*)
			Gerador_Fase3Ind										AT%MX574.4: BOOL;  (*ok*)
			Gerador_Fase3Cap										AT%MX574.5: BOOL;  (*ok*)
			Gerador_TotalInd											AT%MX574.6: BOOL;  (*ok*)
			Gerador_TotalCap										AT%MX574.7: BOOL;  (*ok*)

		CtrlReativo_Info												AT%MW575: INT;
			CtrlReativo_ModoFP										AT%MX575.0: BOOL;  (*ok*)
			CtrlReativo_ModoVAR										AT%MX575.1: BOOL;  (*ok*)

		CtrlPotencia_Info												AT%MW576: INT;
			CtrlPotencia_ModoNivel									AT%MX576.0: BOOL;  (*ok*)
			CtrlPotencia_ModoPotencia								AT%MX576.1: BOOL;  (*ok*)
			CtrlPotencia_ReligamentoAutomatico					AT%MX576.2: BOOL;  (*ok*)

		HorimetroEletrico_Low										AT%MW577: INT;  (*ok*)
		HorimetroEletrico_High										AT%MW578: INT;  (*ok*)

		HorimetroMecanico_Low										AT%MW579: INT;  (*ok*)
		HorimetroMecanico_High									AT%MW580: INT; (*ok*)

		SGI_Info														AT%MW581: INT;

		Temperatura_01												AT%MW582: INT; (* Temperatura da Fase R do Gerador *)
		Temperatura_02												AT%MW583: INT; (* Temperatura da Fase S do Gerador *)
		Temperatura_03												AT%MW584: INT; (* Temperatura da Fase T do Gerador *)
		Temperatura_04												AT%MW585: INT; (* Temperatura Mancal Lado Acoplado do Gerador (Escora 1) *)
		Temperatura_05												AT%MW586: INT; (* Temperatura Mancal Lado Acoplado do Gerador (Escora 2) *)
		Temperatura_06												AT%MW587: INT; (* Temperatura Mancal Lado Acoplado do Gerador (Casquilho) *)
		Temperatura_07												AT%MW588: INT; (* Temperatura Mancal Lado Acoplado do Gerador (Contra-Escora 1) *)
		Temperatura_08												AT%MW589: INT; (* Temperatura Mancal Lado Não Acoplado do Gerador (Casquilho) *)
		Temperatura_09												AT%MW590: INT; (* Temperatura Mancal Lado Acoplado do Gerador (Contra-Esccora 2) *)
		Temperatura_10												AT%MW591: INT; (* Temperatura Vedação do Eixo da Turbina *)
		Temperatura_11												AT%MW592: INT; (* Temperatura do Óleo do Reservatório da UHLM *)
		Temperatura_12												AT%MW593: INT; (* Temperatura do Óleo na Saída do Trocador de Calor *)
		Temperatura_13												AT%MW594: INT; (* Temperatura da Água na Entrada do Trocador de Calor da UHLM *)
		Temperatura_14												AT%MW595: INT; (* Temperatura da Água na Saída do Trocador de Calor da UHLM *)
		Temperatura_15												AT%MW596: INT; (* Temperatura do Óleo do Reservatório da UHCT *)
		Temperatura_16												AT%MW597: INT;

		UHCT_NivelOleo												AT%MW598: INT; (*ok*)

		RegT_FPAlvo													AT%MW599: INT;
		RegT_ReativoAlvo											AT%MW600: INT;

END_VAR

VAR_GLOBAL


		(* -=====    Setpoints    =====- *)

		Setpoints														AT%MW1280 : ARRAY [001..256] OF INT;

		UHCT_PressaoMaxima										AT%MW1280: INT; (*ok*)
		UHCT_PressaoMinima										AT%MW1281: INT; (*ok*)
		UHCT_PressaoDesligamento								AT%MW1282: INT; (*ok*)
		UHCT_PressaoCritica										AT%MW1283: INT; (*ok*)

		CtrlPotencia_NivelL1											AT%MW1284: INT; (*ok*)
		CtrlPotencia_NivelL2											AT%MW1285: INT; (*ok*)
		CtrlPotencia_NivelL3											AT%MW1286: INT; (*ok*)
		CtrlPotencia_NivelL4											AT%MW1287: INT; (*ok*)
		CtrlPotencia_NivelL5											AT%MW1288: INT; (*ok*)

		CtrlPotencia_Potencia1										AT%MW1289: INT; (*ok*)
		CtrlPotencia_Potencia2										AT%MW1290: INT; (*ok*)
		CtrlPotencia_Potencia3										AT%MW1291: INT; (*ok*)
		CtrlPotencia_Potencia4										AT%MW1292: INT; (*ok*)
		CtrlPotencia_Potencia5										AT%MW1293: INT; (*ok*)

		CtrlPotencia_PotenciaMinima								AT%MW1294: INT; (*ok*)
		CtrlPotencia_PotenciaMinimaTempo						AT%MW1295: INT; (*ok*)
		CtrlPotencia_NivelReligamento								AT%MW1296: INT; (*ok*)

		CtrlPotencia_Alvo												AT%MW1297: INT; (*ok*)

		CtrlPotencia_Tolerancia										AT%MW1298: INT; (*ok*)
		CtrlPotencia_PulsoPotencia									AT%MW1299: INT; (*ok*)
		CtrlPotencia_PulsoIntervalo									AT%MW1300: INT; (*ok*)
		CtrlPotencia_SetpointNivel									AT%MW1301: INT; (*ok*)
		CtrlPotencia_NivelMinimoAlarme							AT%MW1302: INT; (*ok*)
		CtrlPotencia_NivelMinimoTRIP								AT%MW1303: INT; (*ok*)

		CtrlReativo_SetpointFP										AT%MW1304: INT; (*ok*)
		CtrlReativo_SetpointReativo									AT%MW1305: INT;(*ok*)

		Turb_Vibracao01Alarme										AT%MW1306: INT;  (*ok*)
		Turb_Vibracao01TRIP										AT%MW1307: INT;  (*ok*)
		Turb_Vibracao02Alarme										AT%MW1308: INT;  (*ok*)
		Turb_Vibracao02TRIP										AT%MW1309: INT;  (*ok*)
		Turb_Vibracao03Alarme										AT%MW1310: INT;
		Turb_Vibracao03TRIP										AT%MW1311: INT;
		Turb_Vibracao04Alarme										AT%MW1312: INT;
		Turb_Vibracao04TRIP										AT%MW1313: INT;

		Turb_TempoEqualizacaoSetpoint							AT%MW1314: INT;(*ok*)

		Freio_PulsoIntervalo											AT%MW1315: INT;
		Freio_PulsoTempo											AT%MW1316: INT;

		UHCT_TempoRodizioLider									AT%MW1317: INT;(*ok*)
		UHCT_TempoRodizioRetaguarda							AT%MW1318: INT;(*ok*)
		UHLM_TempoRodizioLider									AT%MW1319: INT;
		UHLM_TempoRodizioRetaguarda							AT%MW1320: INT;

		Temperatura_01Alarme										AT%MW1321: INT;(*ok*)
		Temperatura_02Alarme										AT%MW1322: INT;(*ok*)
		Temperatura_03Alarme										AT%MW1323: INT;(*ok*)
		Temperatura_04Alarme										AT%MW1324: INT;(*ok*)
		Temperatura_05Alarme										AT%MW1325: INT;(*ok*)
		Temperatura_06Alarme										AT%MW1326: INT;(*ok*)
		Temperatura_07Alarme										AT%MW1327: INT;(*ok*)
		Temperatura_08Alarme										AT%MW1328: INT;(*ok*)
		Temperatura_09Alarme										AT%MW1329: INT;(*ok*)
		Temperatura_10Alarme										AT%MW1330: INT;(*ok*)
		Temperatura_11Alarme										AT%MW1331: INT;(*ok*)
		Temperatura_12Alarme										AT%MW1332: INT;(*ok*)
		Temperatura_13Alarme										AT%MW1333: INT;(*ok*)
		Temperatura_14Alarme										AT%MW1334: INT;(*ok*)
		Temperatura_15Alarme										AT%MW1335: INT;
		Temperatura_16Alarme										AT%MW1336: INT;

		(*=============================================================================================================
			Setpoints de temperaturas apenas para mostrar no supervisório e IHM. O relé de proteção não fornece esses dados via comunicação
		==============================================================================================================*)

		Temperatura_01Trip1										AT%MW1337: INT;(*ok*)
		Temperatura_02Trip1										AT%MW1338: INT;(*ok*)
		Temperatura_03Trip1										AT%MW1339: INT;(*ok*)
		Temperatura_04Trip1										AT%MW1340: INT;(*ok*)
		Temperatura_05Trip1										AT%MW1341: INT;(*ok*)
		Temperatura_06Trip1										AT%MW1342: INT;(*ok*)
		Temperatura_07Trip1										AT%MW1343: INT;(*ok*)
		Temperatura_08Trip1										AT%MW1344: INT;(*ok*)
		Temperatura_09Trip1										AT%MW1345: INT;(*ok*)
		Temperatura_10Trip1										AT%MW1346: INT;(*ok*)
		Temperatura_11Trip1										AT%MW1347: INT;(*ok*)
		Temperatura_12Trip1										AT%MW1348: INT;(*ok*)
		Temperatura_13Trip1										AT%MW1349: INT;(*ok*)
		Temperatura_14Trip1										AT%MW1350: INT;(*ok*)
		Temperatura_15Trip1										AT%MW1351: INT;
		Temperatura_16Trip1										AT%MW1352: INT;

		Temperatura_01Trip2										AT%MW1353: INT;(*ok*)
		Temperatura_02Trip2										AT%MW1354: INT;(*ok*)
		Temperatura_03Trip2										AT%MW1355: INT;(*ok*)
		Temperatura_04Trip2										AT%MW1356: INT;(*ok*)
		Temperatura_05Trip2										AT%MW1357: INT;(*ok*)
		Temperatura_06Trip2										AT%MW1358: INT;(*ok*)
		Temperatura_07Trip2										AT%MW1359: INT;(*ok*)
		Temperatura_08Trip2										AT%MW1360: INT;(*ok*)
		Temperatura_09Trip2										AT%MW1361: INT;(*ok*)
		Temperatura_10Trip2										AT%MW1362: INT;(*ok*)
		Temperatura_11Trip2										AT%MW1363: INT;(*ok*)
		Temperatura_12Trip2										AT%MW1364: INT;(*ok*)
		Temperatura_13Trip2										AT%MW1365: INT;(*ok*)
		Temperatura_14Trip2										AT%MW1366: INT;(*ok*)
		Temperatura_15Trip2										AT%MW1367: INT;
		Temperatura_16Trip2										AT%MW1368: INT;

		UHCT_NivelOleoMinimo									AT%MW1369: INT;(*ok*)

		Turb_Posicao_Distrib_Liga_Aeracao					AT%MW1370: INT;
		Turb_Posicao_Distrib_Desliga_Aeracao				AT%MW1371: INT;

END_VAR

VAR_GLOBAL

		(* -=====    Alarmes    =====- *)

		Alarme													AT%MW1910: ARRAY [01..16] OF WORD;

END_VAR

VAR_GLOBAL

		(* -=====    Analogicas    =====- *)

		Analogicas													AT%MW1990 : ARRAY [001..256] OF INT;

		EA00															AT%MW1990: DT_EntradaAnalogica;
		EA01															AT%MW1998: DT_EntradaAnalogica;
		EA02															AT%MW2006: DT_EntradaAnalogica;
		EA03															AT%MW2014: DT_EntradaAnalogica;
		EA04															AT%MW2022: DT_EntradaAnalogica;
		EA05															AT%MW2030: DT_EntradaAnalogica;
		EA06															AT%MW2038: DT_EntradaAnalogica;
		EA07															AT%MW2046: DT_EntradaAnalogica;
		EA08															AT%MW2054: DT_EntradaAnalogica;
		EA09															AT%MW2062: DT_EntradaAnalogica;
		EA10															AT%MW2070: DT_EntradaAnalogica;
		EA11															AT%MW2078: DT_EntradaAnalogica;
		EA12															AT%MW2086: DT_EntradaAnalogica;
		EA13															AT%MW2094: DT_EntradaAnalogica;
		EA14															AT%MW2102: DT_EntradaAnalogica;
		EA15															AT%MW2110: DT_EntradaAnalogica;

END_VAR

VAR_GLOBAL

		(* Disjuntores Painel PCP-U1 *)

		Disjuntor_01											AT%MW275: INT; 	(* Disjuntor Q125.1 - Alimentação Circuitos de Comando *)
		Disjuntor_02											AT%MW276: INT; 	(* Disjuntor Q125.2 - Alimentação Regulador GRTD2000 *)
		Disjuntor_03											AT%MW277: INT; 	(* Disjuntor Q125.3 - Alimentação Relé de Proteção *)
		Disjuntor_04											AT%MW278: INT; 	(* Disjuntor Q24.0 - Alimentação Válvula Proporcional e Transdutor de Posição *)

		(* Disjuntores CSS-U1 *)

		Disjuntor_05											AT%MW279: INT; 	(* CSS-U1 - Disjuntor Q220.1 - Alimentação Motor Carregamento Mola Disjuntor 52G *)
		Disjuntor_06											AT%MW280: INT; 	(* CSS-U1 - Disjuntor Q125.0 - Alimentação Circuitos de Comando do Disjuntor 52G *)

		(* Disjuntores PDSA *)

		Disjuntor_07											AT%MW281: INT; 	(* PDSA - Disjuntor Motor 1QM1 - Bomba de Óleo 01 da UHCT *)
		Disjuntor_08											AT%MW282: INT;	(* PDSA - Disjuntor Motor 1QM2 - Bomba de Óleo 02 da UHCT *)
		Disjuntor_09											AT%MW283: INT;	(* PDSA - Disjuntor Motor 1QM3 - Bomba de Óleo 01 da UHLM *)
		Disjuntor_10											AT%MW284: INT;	(* PDSA - Disjuntor Motor 1Q380-2 - Resistência de Aquecimento do Óleo da UHLM *)
		Disjuntor_11											AT%MW285: INT;	(* PDSA - Disjuntor Motor 1Q220-4 - Resistência de Aquecimento do Gerador *)

		(* Disjuntores Quadro Q49 *)

		Disjuntor_12											AT%MW286: INT;	(* Q49 - Disjuntor Q125-0 - Módulo de Temperatura SEL2600 *)

		(* Disjuntor 52G  *)

		Disjuntor_13											AT%MW287: INT;	(* Disjuntor 52G *)



END_VAR

=======================================================================================================================
=======================================================================================================================

"""


REG_UG1_Alarme01 = 14199
REG_UG1_Alarme02 = 14200
REG_UG1_Alarme03 = 14201
REG_UG1_Alarme04 = 14202
REG_UG1_Alarme05 = 14203
REG_UG1_Alarme06 = 14204
REG_UG1_Alarme07 = 14205
REG_UG1_Alarme08 = 14206
REG_UG1_Alarme09 = 14207
REG_UG1_Alarme10 = 14208
REG_UG1_Alarme11 = 14209
REG_UG1_Alarme12 = 14210
REG_UG1_Alarme13 = 14211
REG_UG1_Alarme14 = 14212
REG_UG1_Alarme15 = 14213
REG_UG1_Alarme16 = 14214
REG_UG1_CtrlPotencia_Alvo = 13569 + 17 -1
REG_UG1_CtrlPotencia_Info = 12865
REG_UG1_CtrlPotencia_ModoNivelDesligar = 12334
REG_UG1_CtrlPotencia_ModoNivelLigar = 12333
REG_UG1_CtrlPotencia_ModoPotenciaDesligar = 12332
REG_UG1_CtrlPotencia_ModoPotenciaLigar = 12331
REG_UG1_CtrlPotencia_NivelLL1 = 13573
REG_UG1_CtrlPotencia_NivelLL2 = 13574
REG_UG1_CtrlPotencia_NivelLL3 = 13575
REG_UG1_CtrlPotencia_NivelLL4 = 13576
REG_UG1_CtrlPotencia_NivelLL5 = 13577
REG_UG1_CtrlPotencia_NivelMinimoAlarme = 13591
REG_UG1_CtrlPotencia_NivelMinimoTRIP = 13592
REG_UG1_CtrlPotencia_NivelReligamento = 13585
REG_UG1_CtrlPotencia_Potencia1 = 13578
REG_UG1_CtrlPotencia_Potencia2 = 13579
REG_UG1_CtrlPotencia_Potencia3 = 13580
REG_UG1_CtrlPotencia_Potencia4 = 13581
REG_UG1_CtrlPotencia_Potencia5 = 13582
REG_UG1_CtrlPotencia_PotenciaMinima = 13583
REG_UG1_CtrlPotencia_PotenciaMinimaTempo = 13584
REG_UG1_CtrlPotencia_PulsoIntervalo = 13589
REG_UG1_CtrlPotencia_PulsoTempo = 13588
REG_UG1_CtrlPotencia_ReligamentoAutomaticoDesligar = 12336
REG_UG1_CtrlPotencia_ReligamentoAutomaticoLigar = 12335
REG_UG1_CtrlPotencia_SetpointNivel = 13590
REG_UG1_CtrlPotencia_Tolerancia = 13587
REG_UG1_CtrlReativo_Info = 12864
REG_UG1_CtrlReativo_ModoFPDesligar = 12328
REG_UG1_CtrlReativo_ModoFPLigar = 12327
REG_UG1_CtrlReativo_ModoVArDesligar = 12330
REG_UG1_CtrlReativo_ModoVArLigar = 12329
REG_UG1_CtrlReativo_SetpointFP = 13593
REG_UG1_CtrlReativo_SetpointReativo = 13594
REG_UG1_Disj52G_Abrir = 12326
REG_UG1_Disj52G_Info = 12823
REG_UG1_Disjuntor_01 = 12564
REG_UG1_Disjuntor_02 = 12565
REG_UG1_Disjuntor_03 = 12566
REG_UG1_Disjuntor_04 = 12567
REG_UG1_Disjuntor_05 = 12568
REG_UG1_Disjuntor_06 = 12569
REG_UG1_Disjuntor_07 = 12570
REG_UG1_Disjuntor_08 = 12571
REG_UG1_Disjuntor_09 = 12572
REG_UG1_Disjuntor_10 = 12573
REG_UG1_Disjuntor_11 = 12574
REG_UG1_Disjuntor_12 = 12575
REG_UG1_Disjuntor_13 = 12576
REG_UG1_Disjuntor_14 = 12577
REG_UG1_Disjuntor_15 = 12578
REG_UG1_Disjuntor_16 = 12579
REG_UG1_Disjuntor_17 = 12580
REG_UG1_Disjuntor_18 = 12581
REG_UG1_Disjuntor_19 = 12582
REG_UG1_Disjuntor_20 = 12583
REG_UG1_Disjuntor_21 = 12584
REG_UG1_Disjuntor_22 = 12585
REG_UG1_Disjuntor_23 = 12586
REG_UG1_Disjuntor_24 = 12587
REG_UG1_Disjuntor_25 = 12588
REG_UG1_Disjuntor_26 = 12589
REG_UG1_Disjuntor_27 = 12590
REG_UG1_Disjuntor_28 = 12591
REG_UG1_Disjuntor_29 = 12592
REG_UG1_Disjuntor_30 = 12593
REG_UG1_Disjuntor_31 = 12594
REG_UG1_Disjuntor_32 = 12595
REG_UG1_EA00_amostragem = 14285
REG_UG1_EA00_intervalo = 14284
REG_UG1_EA00_offset = 14283
REG_UG1_EA00_x = 14286
REG_UG1_EA00_x0 = 14279
REG_UG1_EA00_x1 = 14280
REG_UG1_EA00_y0 = 14281
REG_UG1_EA00_y1 = 14282
REG_UG1_EA01_amostragem = 14293
REG_UG1_EA01_intervalo = 14292
REG_UG1_EA01_offset = 14291
REG_UG1_EA01_x = 14294
REG_UG1_EA01_x0 = 14287
REG_UG1_EA01_x1 = 14288
REG_UG1_EA01_y0 = 14289
REG_UG1_EA01_y1 = 14290
REG_UG1_EA02_amostragem = 14301
REG_UG1_EA02_intervalo = 14300
REG_UG1_EA02_offset = 14299
REG_UG1_EA02_x = 14302
REG_UG1_EA02_x0 = 14295
REG_UG1_EA02_x1 = 14296
REG_UG1_EA02_y0 = 14297
REG_UG1_EA02_y1 = 14298
REG_UG1_EA03_amostragem = 14309
REG_UG1_EA03_intervalo = 14308
REG_UG1_EA03_offset = 14307
REG_UG1_EA03_x = 14310
REG_UG1_EA03_x0 = 14303
REG_UG1_EA03_x1 = 14304
REG_UG1_EA03_y0 = 14305
REG_UG1_EA03_y1 = 14306
REG_UG1_EA04_amostragem = 14317
REG_UG1_EA04_intervalo = 14316
REG_UG1_EA04_offset = 14315
REG_UG1_EA04_x = 14318
REG_UG1_EA04_x0 = 14311
REG_UG1_EA04_x1 = 14312
REG_UG1_EA04_y0 = 14313
REG_UG1_EA04_y1 = 14314
REG_UG1_EA05_amostragem = 14325
REG_UG1_EA05_intervalo = 14324
REG_UG1_EA05_offset = 14323
REG_UG1_EA05_x = 14326
REG_UG1_EA05_x0 = 14319
REG_UG1_EA05_x1 = 14320
REG_UG1_EA05_y0 = 14321
REG_UG1_EA05_y1 = 14322
REG_UG1_EA06_amostragem = 14333
REG_UG1_EA06_intervalo = 14332
REG_UG1_EA06_offset = 14331
REG_UG1_EA06_x = 14334
REG_UG1_EA06_x0 = 14327
REG_UG1_EA06_x1 = 14328
REG_UG1_EA06_y0 = 14329
REG_UG1_EA06_y1 = 14330
REG_UG1_EA07_amostragem = 14341
REG_UG1_EA07_intervalo = 14340
REG_UG1_EA07_offset = 14339
REG_UG1_EA07_x = 14342
REG_UG1_EA07_x0 = 14335
REG_UG1_EA07_x1 = 14336
REG_UG1_EA07_y0 = 14337
REG_UG1_EA07_y1 = 14338
REG_UG1_EA08_amostragem = 14349
REG_UG1_EA08_intervalo = 14348
REG_UG1_EA08_offset = 14347
REG_UG1_EA08_x = 14350
REG_UG1_EA08_x0 = 14343
REG_UG1_EA08_x1 = 14344
REG_UG1_EA08_y0 = 14345
REG_UG1_EA08_y1 = 14346
REG_UG1_EA09_amostragem = 14357
REG_UG1_EA09_intervalo = 14356
REG_UG1_EA09_offset = 14355
REG_UG1_EA09_x = 14358
REG_UG1_EA09_x0 = 14351
REG_UG1_EA09_x1 = 14352
REG_UG1_EA09_y0 = 14353
REG_UG1_EA09_y1 = 14354
REG_UG1_EA10_amostragem = 14365
REG_UG1_EA10_intervalo = 14364
REG_UG1_EA10_offset = 14363
REG_UG1_EA10_x = 14366
REG_UG1_EA10_x0 = 14359
REG_UG1_EA10_x1 = 14360
REG_UG1_EA10_y0 = 14361
REG_UG1_EA10_y1 = 14362
REG_UG1_EA11_amostragem = 14373
REG_UG1_EA11_intervalo = 14372
REG_UG1_EA11_offset = 14371
REG_UG1_EA11_x = 14374
REG_UG1_EA11_x0 = 14367
REG_UG1_EA11_x1 = 14368
REG_UG1_EA11_y0 = 14369
REG_UG1_EA11_y1 = 14370
REG_UG1_EA12_amostragem = 14381
REG_UG1_EA12_intervalo = 14380
REG_UG1_EA12_offset = 14379
REG_UG1_EA12_x = 14382
REG_UG1_EA12_x0 = 14375
REG_UG1_EA12_x1 = 14376
REG_UG1_EA12_y0 = 14377
REG_UG1_EA12_y1 = 14378
REG_UG1_EA13_amostragem = 14389
REG_UG1_EA13_intervalo = 14388
REG_UG1_EA13_offset = 14387
REG_UG1_EA13_x = 14390
REG_UG1_EA13_x0 = 14383
REG_UG1_EA13_x1 = 14384
REG_UG1_EA13_y0 = 14385
REG_UG1_EA13_y1 = 14386
REG_UG1_EA14_amostragem = 14397
REG_UG1_EA14_intervalo = 14396
REG_UG1_EA14_offset = 14395
REG_UG1_EA14_x = 14398
REG_UG1_EA14_x0 = 14391
REG_UG1_EA14_x1 = 14392
REG_UG1_EA14_y0 = 14393
REG_UG1_EA14_y1 = 14394
REG_UG1_EA15_amostragem = 14405
REG_UG1_EA15_intervalo = 14404
REG_UG1_EA15_offset = 14403
REG_UG1_EA15_x = 14406
REG_UG1_EA15_x0 = 14399
REG_UG1_EA15_x1 = 14400
REG_UG1_EA15_y0 = 14401
REG_UG1_EA15_y1 = 14402
REG_UG1_Freio_PulsoIntervalo = 13604
REG_UG1_Freio_PulsoTempo = 13605
REG_UG1_Gerador_CorrenteMedia = 12833
REG_UG1_Gerador_CorrenteR = 12830
REG_UG1_Gerador_CorrenteS = 12831
REG_UG1_Gerador_CorrenteT = 12832
REG_UG1_Gerador_EnergiaConsumidaGVarh = 12860
REG_UG1_Gerador_EnergiaConsumidaMVarh = 12861
REG_UG1_Gerador_EnergiaConsumidaTVarh = 12859
REG_UG1_Gerador_EnergiaConsumidakVarh = 12862
REG_UG1_Gerador_EnergiaFornecidaGVarh = 12856
REG_UG1_Gerador_EnergiaFornecidaGWh = 12852
REG_UG1_Gerador_EnergiaFornecidaMVarh = 12857
REG_UG1_Gerador_EnergiaFornecidaMWh = 12853
REG_UG1_Gerador_EnergiaFornecidaTVarh = 12855
REG_UG1_Gerador_EnergiaFornecidaTWh = 12851
REG_UG1_Gerador_EnergiaFornecidakVarh = 12858
REG_UG1_Gerador_EnergiaFornecidakWh = 12854
REG_UG1_Gerador_FPInfo = 12863
REG_UG1_Gerador_FatorPotencia1 = 12846
REG_UG1_Gerador_FatorPotencia2 = 12847
REG_UG1_Gerador_FatorPotencia3 = 12848
REG_UG1_Gerador_FatorPotenciaMedia = 12849
REG_UG1_Gerador_Frequencia = 12850
REG_UG1_Gerador_PotenciaAparente1 = 12842
REG_UG1_Gerador_PotenciaAparente2 = 12843
REG_UG1_Gerador_PotenciaAparente3 = 12844
REG_UG1_Gerador_PotenciaAparenteMedia = 12845
REG_UG1_Gerador_PotenciaAtiva1 = 12834
REG_UG1_Gerador_PotenciaAtiva2 = 12835
REG_UG1_Gerador_PotenciaAtiva3 = 12836
REG_UG1_Gerador_PotenciaAtivaMedia = 12837
REG_UG1_Gerador_PotenciaReativa1 = 12838
REG_UG1_Gerador_PotenciaReativa2 = 12839
REG_UG1_Gerador_PotenciaReativa3 = 12840
REG_UG1_Gerador_PotenciaReativaMedia = 12841
REG_UG1_Gerador_TensaoRN = 12824
REG_UG1_Gerador_TensaoRS = 12827
REG_UG1_Gerador_TensaoSN = 12825
REG_UG1_Gerador_TensaoST = 12828
REG_UG1_Gerador_TensaoTN = 12826
REG_UG1_Gerador_TensaoTR = 12829
REG_UG1_HorimetroEletrico_High = 12867
REG_UG1_HorimetroEletrico_Low = 12866
REG_UG1_HorimetroMecanico_High = 12869
REG_UG1_HorimetroMecanico_Low = 12868
REG_UG1_NivelBarragem = 12767
REG_UG1_NivelBarragem = 12767
REG_UG1_NivelCamaraCarga = 12769
REG_UG1_NivelCamaraCarga = 12769
REG_UG1_NivelCanal = 12768
REG_UG1_NivelCanal = 12768
REG_UG1_NivelJusante = 12766
REG_UG1_NivelJusante = 12766
REG_UG1_Operacao_EmergenciaDesligar = 12297
REG_UG1_Operacao_EmergenciaLigar = 12296
REG_UG1_Operacao_EtapaAlvo = 12773
REG_UG1_Operacao_EtapaAtual = 12774
REG_UG1_Operacao_EtapaTransicao = 12775
REG_UG1_Operacao_Info = 12772
REG_UG1_Operacao_InfoParada = 12776
REG_UG1_Operacao_PCH_CovoReconheceAlarmes = 12290
REG_UG1_Operacao_PCH_CovoResetAlarmes = 12289
REG_UG1_Operacao_PainelReconheceAlarmes = 12771
REG_UG1_Operacao_PainelResetAlarmes = 12770
REG_UG1_Operacao_ParadaReset = 12361
REG_UG1_Operacao_UP = 12291
REG_UG1_Operacao_UPGM = 12292
REG_UG1_Operacao_UPS = 12294
REG_UG1_Operacao_US = 12295
REG_UG1_Operacao_UVD = 12293
REG_UG1_RegT_DecrementaTensao = 12319
REG_UG1_RegT_Desligar = 12317
REG_UG1_RegT_IExcitacao = 12817
REG_UG1_RegT_IncrementaTensao = 12318
REG_UG1_RegT_Info = 12815
REG_UG1_RegT_Ligar = 12316
REG_UG1_RegT_PreExcitacao = 12320
REG_UG1_RegT_UExcitacao = 12816
REG_UG1_RegV_ColocarCarga = 12310
REG_UG1_RegV_DecrementaVelocidade = 12313
REG_UG1_RegV_Distribuidor = 12812
REG_UG1_RegV_Estado = 12810
REG_UG1_RegV_IncrementaVelocidade = 12312
REG_UG1_RegV_Info = 12809
REG_UG1_RegV_Parar = 12309
REG_UG1_RegV_Partir = 12308
REG_UG1_RegV_PotenciaAlvo = 12814
REG_UG1_RegV_RetirarCarga = 12311
REG_UG1_RegV_Rotor = 12813
REG_UG1_RegV_SelecionaModoBaseCarga = 12315
REG_UG1_RegV_SelecionaModoEstatismo = 12314
REG_UG1_RegV_Velocidade = 12811
REG_UG1_SGI_Info = 12870
REG_UG1_Sinc_Desligar = 12322
REG_UG1_Sinc_FrequenciaBarra = 12820
REG_UG1_Sinc_FrequenciaGerador = 12819
REG_UG1_Sinc_Info = 12818
REG_UG1_Sinc_Ligar = 12321
REG_UG1_Sinc_ModoAutoLigar = 12323
REG_UG1_Sinc_ModoBMortaLigar = 12325
REG_UG1_Sinc_ModoManualLigar = 12324
REG_UG1_Sinc_TensaoBarra = 12822
REG_UG1_Sinc_TensaoGerador = 12821
REG_UG1_Temperatura01_Alarme = 13610
REG_UG1_Temperatura01_TRIP01 = 13626
REG_UG1_Temperatura01_TRIP02 = 13642
REG_UG1_Temperatura02_Alarme = 13611
REG_UG1_Temperatura02_TRIP01 = 13627
REG_UG1_Temperatura02_TRIP02 = 13643
REG_UG1_Temperatura03_Alarme = 13612
REG_UG1_Temperatura03_TRIP01 = 13628
REG_UG1_Temperatura03_TRIP02 = 13644
REG_UG1_Temperatura04_Alarme = 13613
REG_UG1_Temperatura04_TRIP01 = 13629
REG_UG1_Temperatura04_TRIP02 = 13645
REG_UG1_Temperatura05_Alarme = 13614
REG_UG1_Temperatura05_TRIP01 = 13630
REG_UG1_Temperatura05_TRIP02 = 13646
REG_UG1_Temperatura06_Alarme = 13615
REG_UG1_Temperatura06_TRIP01 = 13631
REG_UG1_Temperatura06_TRIP02 = 13647
REG_UG1_Temperatura07_Alarme = 13616
REG_UG1_Temperatura07_TRIP01 = 13632
REG_UG1_Temperatura07_TRIP02 = 13648
REG_UG1_Temperatura08_Alarme = 13617
REG_UG1_Temperatura08_TRIP01 = 13633
REG_UG1_Temperatura08_TRIP02 = 13649
REG_UG1_Temperatura09_Alarme = 13618
REG_UG1_Temperatura09_TRIP01 = 13634
REG_UG1_Temperatura09_TRIP02 = 13650
REG_UG1_Temperatura10_Alarme = 13619
REG_UG1_Temperatura10_TRIP01 = 13635
REG_UG1_Temperatura10_TRIP02 = 13651
REG_UG1_Temperatura11_Alarme = 13620
REG_UG1_Temperatura11_TRIP01 = 13636
REG_UG1_Temperatura11_TRIP02 = 13652
REG_UG1_Temperatura12_Alarme = 13621
REG_UG1_Temperatura12_TRIP01 = 13637
REG_UG1_Temperatura12_TRIP02 = 13653
REG_UG1_Temperatura13_Alarme = 13622
REG_UG1_Temperatura13_TRIP01 = 13638
REG_UG1_Temperatura13_TRIP02 = 13654
REG_UG1_Temperatura14_Alarme = 13623
REG_UG1_Temperatura14_TRIP01 = 13639
REG_UG1_Temperatura14_TRIP02 = 13655
REG_UG1_Temperatura15_Alarme = 13624
REG_UG1_Temperatura15_TRIP01 = 13640
REG_UG1_Temperatura15_TRIP02 = 13656
REG_UG1_Temperatura16_Alarme = 13625
REG_UG1_Temperatura16_TRIP01 = 13641
REG_UG1_Temperatura16_TRIP02 = 13657
REG_UG1_Temperatura_01 = 12871
REG_UG1_Temperatura_02 = 12872
REG_UG1_Temperatura_03 = 12873
REG_UG1_Temperatura_04 = 12874
REG_UG1_Temperatura_05 = 12875
REG_UG1_Temperatura_06 = 12876
REG_UG1_Temperatura_07 = 12877
REG_UG1_Temperatura_08 = 12878
REG_UG1_Temperatura_09 = 12879
REG_UG1_Temperatura_10 = 12880
REG_UG1_Temperatura_11 = 12881
REG_UG1_Temperatura_12 = 12882
REG_UG1_Temperatura_13 = 12883
REG_UG1_Temperatura_14 = 12884
REG_UG1_Temperatura_15 = 12885
REG_UG1_Temperatura_16 = 12886
REG_UG1_Turb_BorboletaAbrir = 12300
REG_UG1_Turb_BorboletaFechar = 12301
REG_UG1_Turb_ByPassAbrir = 12298
REG_UG1_Turb_ByPassFechar = 12299
REG_UG1_Turb_Frenagem = 12808
REG_UG1_Turb_FrenagemAplicar = 12302
REG_UG1_Turb_FrenagemAuto = 12305
REG_UG1_Turb_FrenagemDesaplicar = 12303
REG_UG1_Turb_FrenagemManual = 12304
REG_UG1_Turb_Info = 12796
REG_UG1_Turb_PosicaoDistribDesligaAeracao = 13660
REG_UG1_Turb_PosicaoDistribLigaAeracao = 13659
REG_UG1_Turb_PressaoCaixaEspiral = 12802
REG_UG1_Turb_PressaoConduto = 12801
REG_UG1_Turb_SensorAtivar = 12306
REG_UG1_Turb_SensorDesativar = 12307
REG_UG1_Turb_TempoCrackEfetivo = 12799
REG_UG1_Turb_TempoEqualizacaoEfetivo = 12800
REG_UG1_Turb_TempoEqualizacaoSetpoint = 13603
REG_UG1_Turb_ValvulaBorboleta = 12798
REG_UG1_Turb_ValvulaByPass = 12797
REG_UG1_Turb_VazaoTurbinada = 12803
REG_UG1_Turb_Vibracao01 = 12804
REG_UG1_Turb_Vibracao01Alarme = 13595
REG_UG1_Turb_Vibracao01TRIP = 13596
REG_UG1_Turb_Vibracao02 = 12805
REG_UG1_Turb_Vibracao02Alarme = 13597
REG_UG1_Turb_Vibracao02TRIP = 13598
REG_UG1_Turb_Vibracao03 = 12806
REG_UG1_Turb_Vibracao03Alarme = 13599
REG_UG1_Turb_Vibracao03TRIP = 13600
REG_UG1_Turb_Vibracao04 = 12807
REG_UG1_Turb_Vibracao04Alarme = 13601
REG_UG1_Turb_Vibracao04TRIP = 13602
REG_UG1_UHCT_AcumuladorRodizioPrincipal = 12785
REG_UG1_UHCT_AcumuladorRodizioRetaguarda = 12786
REG_UG1_UHCT_Bomba01Desligar = 12338
REG_UG1_UHCT_Bomba01Ligar = 12337
REG_UG1_UHCT_Bomba01Principal = 12339
REG_UG1_UHCT_Bomba02Desligar = 12341
REG_UG1_UHCT_Bomba02Ligar = 12340
REG_UG1_UHCT_Bomba02Principal = 12342
REG_UG1_UHCT_BombaAguaDesligar = 12344
REG_UG1_UHCT_BombaAguaLigar = 12343
REG_UG1_UHCT_Bombas = 12778
REG_UG1_UHCT_Filtros = 12781
REG_UG1_UHCT_Info = 12777
REG_UG1_UHCT_Nivel = 12783
REG_UG1_UHCT_NivelOleo = 12887
REG_UG1_UHCT_NivelOleoMinimo = 13658
REG_UG1_UHCT_PressaoCritica = 13572
REG_UG1_UHCT_PressaoDesligamento = 13571
REG_UG1_UHCT_PressaoMaxima = 13569
REG_UG1_UHCT_PressaoMinima = 13570
REG_UG1_UHCT_PressaoOleo = 12784
REG_UG1_UHCT_Pressostatos = 12782
REG_UG1_UHCT_Rodizio = 12779
REG_UG1_UHCT_RodizioDesabilitar = 12348
REG_UG1_UHCT_RodizioHabilitar = 12347
REG_UG1_UHCT_RodizioPrincipal = 13606
REG_UG1_UHCT_RodizioRetaguarda = 13607
REG_UG1_UHCT_SensorAtivar = 12345
REG_UG1_UHCT_SensorDesativar = 12346
REG_UG1_UHCT_Valvulas = 12780
REG_UG1_UHLM_AcumuladorRodizioPrincipal = 12794
REG_UG1_UHLM_AcumuladorRodizioRetaguarda = 12795
REG_UG1_UHLM_Bomba01Desligar = 12350
REG_UG1_UHLM_Bomba01Ligar = 12349
REG_UG1_UHLM_Bomba01Principal = 12351
REG_UG1_UHLM_Bomba02Desligar = 12353
REG_UG1_UHLM_Bomba02Ligar = 12352
REG_UG1_UHLM_Bomba02Principal = 12354
REG_UG1_UHLM_BombaAguaDesliga = 12358
REG_UG1_UHLM_BombaAguaLiga = 12357
REG_UG1_UHLM_BombaJackingDesliga = 12356
REG_UG1_UHLM_BombaJackingLiga = 12355
REG_UG1_UHLM_Bombas = 12788
REG_UG1_UHLM_Filtros = 12790
REG_UG1_UHLM_Fluxostatos = 12792
REG_UG1_UHLM_Info = 12787
REG_UG1_UHLM_Nivel = 12793
REG_UG1_UHLM_Pressostatos = 12791
REG_UG1_UHLM_Rodizio = 12789
REG_UG1_UHLM_RodizioDesabilitar = 12360
REG_UG1_UHLM_RodizioHabilitar = 12359
REG_UG1_UHLM_RodizioPrincipal = 13608
REG_UG1_UHLM_RodizioRetaguarda = 13609
REG_UG1_VersaoBase = 12764
REG_UG1_VersaoCustom = 12765
REG_UG2_Alarme01 = 14199
REG_UG2_Alarme02 = 14200
REG_UG2_Alarme03 = 14201
REG_UG2_Alarme04 = 14202
REG_UG2_Alarme05 = 14203
REG_UG2_Alarme06 = 14204
REG_UG2_Alarme07 = 14205
REG_UG2_Alarme08 = 14206
REG_UG2_Alarme09 = 14207
REG_UG2_Alarme10 = 14208
REG_UG2_Alarme11 = 14209
REG_UG2_Alarme12 = 14210
REG_UG2_Alarme13 = 14211
REG_UG2_Alarme14 = 14212
REG_UG2_Alarme15 = 14213
REG_UG2_Alarme16 = 14214
REG_UG2_CtrlPotencia_Alvo = 13569 + 17
REG_UG2_CtrlPotencia_Info = 12865
REG_UG2_CtrlPotencia_ModoNivelDesligar = 12334
REG_UG2_CtrlPotencia_ModoNivelLigar = 12333
REG_UG2_CtrlPotencia_ModoPotenciaDesligar = 12332
REG_UG2_CtrlPotencia_ModoPotenciaLigar = 12331
REG_UG2_CtrlPotencia_NivelLL1 = 13573
REG_UG2_CtrlPotencia_NivelLL2 = 13574
REG_UG2_CtrlPotencia_NivelLL3 = 13575
REG_UG2_CtrlPotencia_NivelLL4 = 13576
REG_UG2_CtrlPotencia_NivelLL5 = 13577
REG_UG2_CtrlPotencia_NivelMinimoAlarme = 13591
REG_UG2_CtrlPotencia_NivelMinimoTRIP = 13592
REG_UG2_CtrlPotencia_NivelReligamento = 13585
REG_UG2_CtrlPotencia_Potencia1 = 13578
REG_UG2_CtrlPotencia_Potencia2 = 13579
REG_UG2_CtrlPotencia_Potencia3 = 13580
REG_UG2_CtrlPotencia_Potencia4 = 13581
REG_UG2_CtrlPotencia_Potencia5 = 13582
REG_UG2_CtrlPotencia_PotenciaMinima = 13583
REG_UG2_CtrlPotencia_PotenciaMinimaTempo = 13584
REG_UG2_CtrlPotencia_PulsoIntervalo = 13589
REG_UG2_CtrlPotencia_PulsoTempo = 13588
REG_UG2_CtrlPotencia_ReligamentoAutomaticoDesligar = 12336
REG_UG2_CtrlPotencia_ReligamentoAutomaticoLigar = 12335
REG_UG2_CtrlPotencia_SetpointNivel = 13590
REG_UG2_CtrlPotencia_Tolerancia = 13587
REG_UG2_CtrlReativo_Info = 12864
REG_UG2_CtrlReativo_ModoFPDesligar = 12328
REG_UG2_CtrlReativo_ModoFPLigar = 12327
REG_UG2_CtrlReativo_ModoVArDesligar = 12330
REG_UG2_CtrlReativo_ModoVArLigar = 12329
REG_UG2_CtrlReativo_SetpointFP = 13593
REG_UG2_CtrlReativo_SetpointReativo = 13594
REG_UG2_Disj52G_Abrir = 12326
REG_UG2_Disj52G_Info = 12823
REG_UG2_Disjuntor_01 = 12564
REG_UG2_Disjuntor_02 = 12565
REG_UG2_Disjuntor_03 = 12566
REG_UG2_Disjuntor_04 = 12567
REG_UG2_Disjuntor_05 = 12568
REG_UG2_Disjuntor_06 = 12569
REG_UG2_Disjuntor_07 = 12570
REG_UG2_Disjuntor_08 = 12571
REG_UG2_Disjuntor_09 = 12572
REG_UG2_Disjuntor_10 = 12573
REG_UG2_Disjuntor_11 = 12574
REG_UG2_Disjuntor_12 = 12575
REG_UG2_Disjuntor_13 = 12576
REG_UG2_Disjuntor_14 = 12577
REG_UG2_Disjuntor_15 = 12578
REG_UG2_Disjuntor_16 = 12579
REG_UG2_Disjuntor_17 = 12580
REG_UG2_Disjuntor_18 = 12581
REG_UG2_Disjuntor_19 = 12582
REG_UG2_Disjuntor_20 = 12583
REG_UG2_Disjuntor_21 = 12584
REG_UG2_Disjuntor_22 = 12585
REG_UG2_Disjuntor_23 = 12586
REG_UG2_Disjuntor_24 = 12587
REG_UG2_Disjuntor_25 = 12588
REG_UG2_Disjuntor_26 = 12589
REG_UG2_Disjuntor_27 = 12590
REG_UG2_Disjuntor_28 = 12591
REG_UG2_Disjuntor_29 = 12592
REG_UG2_Disjuntor_30 = 12593
REG_UG2_Disjuntor_31 = 12594
REG_UG2_Disjuntor_32 = 12595
REG_UG2_EA00_amostragem = 14285
REG_UG2_EA00_intervalo = 14284
REG_UG2_EA00_offset = 14283
REG_UG2_EA00_x = 14286
REG_UG2_EA00_x0 = 14279
REG_UG2_EA00_x1 = 14280
REG_UG2_EA00_y0 = 14281
REG_UG2_EA00_y1 = 14282
REG_UG2_EA01_amostragem = 14293
REG_UG2_EA01_intervalo = 14292
REG_UG2_EA01_offset = 14291
REG_UG2_EA01_x = 14294
REG_UG2_EA01_x0 = 14287
REG_UG2_EA01_x1 = 14288
REG_UG2_EA01_y0 = 14289
REG_UG2_EA01_y1 = 14290
REG_UG2_EA02_amostragem = 14301
REG_UG2_EA02_intervalo = 14300
REG_UG2_EA02_offset = 14299
REG_UG2_EA02_x = 14302
REG_UG2_EA02_x0 = 14295
REG_UG2_EA02_x1 = 14296
REG_UG2_EA02_y0 = 14297
REG_UG2_EA02_y1 = 14298
REG_UG2_EA03_amostragem = 14309
REG_UG2_EA03_intervalo = 14308
REG_UG2_EA03_offset = 14307
REG_UG2_EA03_x = 14310
REG_UG2_EA03_x0 = 14303
REG_UG2_EA03_x1 = 14304
REG_UG2_EA03_y0 = 14305
REG_UG2_EA03_y1 = 14306
REG_UG2_EA04_amostragem = 14317
REG_UG2_EA04_intervalo = 14316
REG_UG2_EA04_offset = 14315
REG_UG2_EA04_x = 14318
REG_UG2_EA04_x0 = 14311
REG_UG2_EA04_x1 = 14312
REG_UG2_EA04_y0 = 14313
REG_UG2_EA04_y1 = 14314
REG_UG2_EA05_amostragem = 14325
REG_UG2_EA05_intervalo = 14324
REG_UG2_EA05_offset = 14323
REG_UG2_EA05_x = 14326
REG_UG2_EA05_x0 = 14319
REG_UG2_EA05_x1 = 14320
REG_UG2_EA05_y0 = 14321
REG_UG2_EA05_y1 = 14322
REG_UG2_EA06_amostragem = 14333
REG_UG2_EA06_intervalo = 14332
REG_UG2_EA06_offset = 14331
REG_UG2_EA06_x = 14334
REG_UG2_EA06_x0 = 14327
REG_UG2_EA06_x1 = 14328
REG_UG2_EA06_y0 = 14329
REG_UG2_EA06_y1 = 14330
REG_UG2_EA07_amostragem = 14341
REG_UG2_EA07_intervalo = 14340
REG_UG2_EA07_offset = 14339
REG_UG2_EA07_x = 14342
REG_UG2_EA07_x0 = 14335
REG_UG2_EA07_x1 = 14336
REG_UG2_EA07_y0 = 14337
REG_UG2_EA07_y1 = 14338
REG_UG2_EA08_amostragem = 14349
REG_UG2_EA08_intervalo = 14348
REG_UG2_EA08_offset = 14347
REG_UG2_EA08_x = 14350
REG_UG2_EA08_x0 = 14343
REG_UG2_EA08_x1 = 14344
REG_UG2_EA08_y0 = 14345
REG_UG2_EA08_y1 = 14346
REG_UG2_EA09_amostragem = 14357
REG_UG2_EA09_intervalo = 14356
REG_UG2_EA09_offset = 14355
REG_UG2_EA09_x = 14358
REG_UG2_EA09_x0 = 14351
REG_UG2_EA09_x1 = 14352
REG_UG2_EA09_y0 = 14353
REG_UG2_EA09_y1 = 14354
REG_UG2_EA10_amostragem = 14365
REG_UG2_EA10_intervalo = 14364
REG_UG2_EA10_offset = 14363
REG_UG2_EA10_x = 14366
REG_UG2_EA10_x0 = 14359
REG_UG2_EA10_x1 = 14360
REG_UG2_EA10_y0 = 14361
REG_UG2_EA10_y1 = 14362
REG_UG2_EA11_amostragem = 14373
REG_UG2_EA11_intervalo = 14372
REG_UG2_EA11_offset = 14371
REG_UG2_EA11_x = 14374
REG_UG2_EA11_x0 = 14367
REG_UG2_EA11_x1 = 14368
REG_UG2_EA11_y0 = 14369
REG_UG2_EA11_y1 = 14370
REG_UG2_EA12_amostragem = 14381
REG_UG2_EA12_intervalo = 14380
REG_UG2_EA12_offset = 14379
REG_UG2_EA12_x = 14382
REG_UG2_EA12_x0 = 14375
REG_UG2_EA12_x1 = 14376
REG_UG2_EA12_y0 = 14377
REG_UG2_EA12_y1 = 14378
REG_UG2_EA13_amostragem = 14389
REG_UG2_EA13_intervalo = 14388
REG_UG2_EA13_offset = 14387
REG_UG2_EA13_x = 14390
REG_UG2_EA13_x0 = 14383
REG_UG2_EA13_x1 = 14384
REG_UG2_EA13_y0 = 14385
REG_UG2_EA13_y1 = 14386
REG_UG2_EA14_amostragem = 14397
REG_UG2_EA14_intervalo = 14396
REG_UG2_EA14_offset = 14395
REG_UG2_EA14_x = 14398
REG_UG2_EA14_x0 = 14391
REG_UG2_EA14_x1 = 14392
REG_UG2_EA14_y0 = 14393
REG_UG2_EA14_y1 = 14394
REG_UG2_EA15_amostragem = 14405
REG_UG2_EA15_intervalo = 14404
REG_UG2_EA15_offset = 14403
REG_UG2_EA15_x = 14406
REG_UG2_EA15_x0 = 14399
REG_UG2_EA15_x1 = 14400
REG_UG2_EA15_y0 = 14401
REG_UG2_EA15_y1 = 14402
REG_UG2_Freio_PulsoIntervalo = 13604
REG_UG2_Freio_PulsoTempo = 13605
REG_UG2_Gerador_CorrenteMedia = 12833
REG_UG2_Gerador_CorrenteR = 12830
REG_UG2_Gerador_CorrenteS = 12831
REG_UG2_Gerador_CorrenteT = 12832
REG_UG2_Gerador_EnergiaConsumidaGVarh = 12860
REG_UG2_Gerador_EnergiaConsumidaMVarh = 12861
REG_UG2_Gerador_EnergiaConsumidaTVarh = 12859
REG_UG2_Gerador_EnergiaConsumidakVarh = 12862
REG_UG2_Gerador_EnergiaFornecidaGVarh = 12856
REG_UG2_Gerador_EnergiaFornecidaGWh = 12852
REG_UG2_Gerador_EnergiaFornecidaMVarh = 12857
REG_UG2_Gerador_EnergiaFornecidaMWh = 12853
REG_UG2_Gerador_EnergiaFornecidaTVarh = 12855
REG_UG2_Gerador_EnergiaFornecidaTWh = 12851
REG_UG2_Gerador_EnergiaFornecidakVarh = 12858
REG_UG2_Gerador_EnergiaFornecidakWh = 12854
REG_UG2_Gerador_FPInfo = 12863
REG_UG2_Gerador_FatorPotencia1 = 12846
REG_UG2_Gerador_FatorPotencia2 = 12847
REG_UG2_Gerador_FatorPotencia3 = 12848
REG_UG2_Gerador_FatorPotenciaMedia = 12849
REG_UG2_Gerador_Frequencia = 12850
REG_UG2_Gerador_PotenciaAparente1 = 12842
REG_UG2_Gerador_PotenciaAparente2 = 12843
REG_UG2_Gerador_PotenciaAparente3 = 12844
REG_UG2_Gerador_PotenciaAparenteMedia = 12845
REG_UG2_Gerador_PotenciaAtiva1 = 12834
REG_UG2_Gerador_PotenciaAtiva2 = 12835
REG_UG2_Gerador_PotenciaAtiva3 = 12836
REG_UG2_Gerador_PotenciaAtivaMedia = 12837
REG_UG2_Gerador_PotenciaReativa1 = 12838
REG_UG2_Gerador_PotenciaReativa2 = 12839
REG_UG2_Gerador_PotenciaReativa3 = 12840
REG_UG2_Gerador_PotenciaReativaMedia = 12841
REG_UG2_Gerador_TensaoRN = 12824
REG_UG2_Gerador_TensaoRS = 12827
REG_UG2_Gerador_TensaoSN = 12825
REG_UG2_Gerador_TensaoST = 12828
REG_UG2_Gerador_TensaoTN = 12826
REG_UG2_Gerador_TensaoTR = 12829
REG_UG2_HorimetroEletrico_High = 12867
REG_UG2_HorimetroEletrico_Low = 12866
REG_UG2_HorimetroMecanico_High = 12869
REG_UG2_HorimetroMecanico_Low = 12868
REG_UG2_NivelBarragem = 12767
REG_UG2_NivelBarragem = 12767
REG_UG2_NivelCamaraCarga = 12769
REG_UG2_NivelCamaraCarga = 12769
REG_UG2_NivelCanal = 12768
REG_UG2_NivelCanal = 12768
REG_UG2_NivelJusante = 12766
REG_UG2_NivelJusante = 12766
REG_UG2_Operacao_EmergenciaDesligar = 12297
REG_UG2_Operacao_EmergenciaLigar = 12296
REG_UG2_Operacao_EtapaAlvo = 12773
REG_UG2_Operacao_EtapaAtual = 12774
REG_UG2_Operacao_EtapaTransicao = 12775
REG_UG2_Operacao_Info = 12772
REG_UG2_Operacao_InfoParada = 12776
REG_UG2_Operacao_PCH_CovoReconheceAlarmes = 12290
REG_UG2_Operacao_PCH_CovoResetAlarmes = 12289
REG_UG2_Operacao_PainelReconheceAlarmes = 12771
REG_UG2_Operacao_PainelResetAlarmes = 12770
REG_UG2_Operacao_ParadaReset = 12361
REG_UG2_Operacao_UP = 12291
REG_UG2_Operacao_UPGM = 12292
REG_UG2_Operacao_UPS = 12294
REG_UG2_Operacao_US = 12295
REG_UG2_Operacao_UVD = 12293
REG_UG2_RegT_DecrementaTensao = 12319
REG_UG2_RegT_Desligar = 12317
REG_UG2_RegT_IExcitacao = 12817
REG_UG2_RegT_IncrementaTensao = 12318
REG_UG2_RegT_Info = 12815
REG_UG2_RegT_Ligar = 12316
REG_UG2_RegT_PreExcitacao = 12320
REG_UG2_RegT_UExcitacao = 12816
REG_UG2_RegV_ColocarCarga = 12310
REG_UG2_RegV_DecrementaVelocidade = 12313
REG_UG2_RegV_Distribuidor = 12812
REG_UG2_RegV_Estado = 12810
REG_UG2_RegV_IncrementaVelocidade = 12312
REG_UG2_RegV_Info = 12809
REG_UG2_RegV_Parar = 12309
REG_UG2_RegV_Partir = 12308
REG_UG2_RegV_PotenciaAlvo = 12814
REG_UG2_RegV_RetirarCarga = 12311
REG_UG2_RegV_Rotor = 12813
REG_UG2_RegV_SelecionaModoBaseCarga = 12315
REG_UG2_RegV_SelecionaModoEstatismo = 12314
REG_UG2_RegV_Velocidade = 12811
REG_UG2_SGI_Info = 12870
REG_UG2_Sinc_Desligar = 12322
REG_UG2_Sinc_FrequenciaBarra = 12820
REG_UG2_Sinc_FrequenciaGerador = 12819
REG_UG2_Sinc_Info = 12818
REG_UG2_Sinc_Ligar = 12321
REG_UG2_Sinc_ModoAutoLigar = 12323
REG_UG2_Sinc_ModoBMortaLigar = 12325
REG_UG2_Sinc_ModoManualLigar = 12324
REG_UG2_Sinc_TensaoBarra = 12822
REG_UG2_Sinc_TensaoGerador = 12821
REG_UG2_Temperatura01_Alarme = 13610
REG_UG2_Temperatura01_TRIP01 = 13626
REG_UG2_Temperatura01_TRIP02 = 13642
REG_UG2_Temperatura02_Alarme = 13611
REG_UG2_Temperatura02_TRIP01 = 13627
REG_UG2_Temperatura02_TRIP02 = 13643
REG_UG2_Temperatura03_Alarme = 13612
REG_UG2_Temperatura03_TRIP01 = 13628
REG_UG2_Temperatura03_TRIP02 = 13644
REG_UG2_Temperatura04_Alarme = 13613
REG_UG2_Temperatura04_TRIP01 = 13629
REG_UG2_Temperatura04_TRIP02 = 13645
REG_UG2_Temperatura05_Alarme = 13614
REG_UG2_Temperatura05_TRIP01 = 13630
REG_UG2_Temperatura05_TRIP02 = 13646
REG_UG2_Temperatura06_Alarme = 13615
REG_UG2_Temperatura06_TRIP01 = 13631
REG_UG2_Temperatura06_TRIP02 = 13647
REG_UG2_Temperatura07_Alarme = 13616
REG_UG2_Temperatura07_TRIP01 = 13632
REG_UG2_Temperatura07_TRIP02 = 13648
REG_UG2_Temperatura08_Alarme = 13617
REG_UG2_Temperatura08_TRIP01 = 13633
REG_UG2_Temperatura08_TRIP02 = 13649
REG_UG2_Temperatura09_Alarme = 13618
REG_UG2_Temperatura09_TRIP01 = 13634
REG_UG2_Temperatura09_TRIP02 = 13650
REG_UG2_Temperatura10_Alarme = 13619
REG_UG2_Temperatura10_TRIP01 = 13635
REG_UG2_Temperatura10_TRIP02 = 13651
REG_UG2_Temperatura11_Alarme = 13620
REG_UG2_Temperatura11_TRIP01 = 13636
REG_UG2_Temperatura11_TRIP02 = 13652
REG_UG2_Temperatura12_Alarme = 13621
REG_UG2_Temperatura12_TRIP01 = 13637
REG_UG2_Temperatura12_TRIP02 = 13653
REG_UG2_Temperatura13_Alarme = 13622
REG_UG2_Temperatura13_TRIP01 = 13638
REG_UG2_Temperatura13_TRIP02 = 13654
REG_UG2_Temperatura14_Alarme = 13623
REG_UG2_Temperatura14_TRIP01 = 13639
REG_UG2_Temperatura14_TRIP02 = 13655
REG_UG2_Temperatura15_Alarme = 13624
REG_UG2_Temperatura15_TRIP01 = 13640
REG_UG2_Temperatura15_TRIP02 = 13656
REG_UG2_Temperatura16_Alarme = 13625
REG_UG2_Temperatura16_TRIP01 = 13641
REG_UG2_Temperatura16_TRIP02 = 13657
REG_UG2_Temperatura_01 = 12871
REG_UG2_Temperatura_02 = 12872
REG_UG2_Temperatura_03 = 12873
REG_UG2_Temperatura_04 = 12874
REG_UG2_Temperatura_05 = 12875
REG_UG2_Temperatura_06 = 12876
REG_UG2_Temperatura_07 = 12877
REG_UG2_Temperatura_08 = 12878
REG_UG2_Temperatura_09 = 12879
REG_UG2_Temperatura_10 = 12880
REG_UG2_Temperatura_11 = 12881
REG_UG2_Temperatura_12 = 12882
REG_UG2_Temperatura_13 = 12883
REG_UG2_Temperatura_14 = 12884
REG_UG2_Temperatura_15 = 12885
REG_UG2_Temperatura_16 = 12886
REG_UG2_Turb_BorboletaAbrir = 12300
REG_UG2_Turb_BorboletaFechar = 12301
REG_UG2_Turb_ByPassAbrir = 12298
REG_UG2_Turb_ByPassFechar = 12299
REG_UG2_Turb_Frenagem = 12808
REG_UG2_Turb_FrenagemAplicar = 12302
REG_UG2_Turb_FrenagemAuto = 12305
REG_UG2_Turb_FrenagemDesaplicar = 12303
REG_UG2_Turb_FrenagemManual = 12304
REG_UG2_Turb_Info = 12796
REG_UG2_Turb_PosicaoDistribDesligaAeracao = 13660
REG_UG2_Turb_PosicaoDistribLigaAeracao = 13659
REG_UG2_Turb_PressaoCaixaEspiral = 12802
REG_UG2_Turb_PressaoConduto = 12801
REG_UG2_Turb_SensorAtivar = 12306
REG_UG2_Turb_SensorDesativar = 12307
REG_UG2_Turb_TempoCrackEfetivo = 12799
REG_UG2_Turb_TempoEqualizacaoEfetivo = 12800
REG_UG2_Turb_TempoEqualizacaoSetpoint = 13603
REG_UG2_Turb_ValvulaBorboleta = 12798
REG_UG2_Turb_ValvulaByPass = 12797
REG_UG2_Turb_VazaoTurbinada = 12803
REG_UG2_Turb_Vibracao01 = 12804
REG_UG2_Turb_Vibracao01Alarme = 13595
REG_UG2_Turb_Vibracao01TRIP = 13596
REG_UG2_Turb_Vibracao02 = 12805
REG_UG2_Turb_Vibracao02Alarme = 13597
REG_UG2_Turb_Vibracao02TRIP = 13598
REG_UG2_Turb_Vibracao03 = 12806
REG_UG2_Turb_Vibracao03Alarme = 13599
REG_UG2_Turb_Vibracao03TRIP = 13600
REG_UG2_Turb_Vibracao04 = 12807
REG_UG2_Turb_Vibracao04Alarme = 13601
REG_UG2_Turb_Vibracao04TRIP = 13602
REG_UG2_UHCT_AcumuladorRodizioPrincipal = 12785
REG_UG2_UHCT_AcumuladorRodizioRetaguarda = 12786
REG_UG2_UHCT_Bomba01Desligar = 12338
REG_UG2_UHCT_Bomba01Ligar = 12337
REG_UG2_UHCT_Bomba01Principal = 12339
REG_UG2_UHCT_Bomba02Desligar = 12341
REG_UG2_UHCT_Bomba02Ligar = 12340
REG_UG2_UHCT_Bomba02Principal = 12342
REG_UG2_UHCT_BombaAguaDesligar = 12344
REG_UG2_UHCT_BombaAguaLigar = 12343
REG_UG2_UHCT_Bombas = 12778
REG_UG2_UHCT_Filtros = 12781
REG_UG2_UHCT_Info = 12777
REG_UG2_UHCT_Nivel = 12783
REG_UG2_UHCT_NivelOleo = 12887
REG_UG2_UHCT_NivelOleoMinimo = 13658
REG_UG2_UHCT_PressaoCritica = 13572
REG_UG2_UHCT_PressaoDesligamento = 13571
REG_UG2_UHCT_PressaoMaxima = 13569
REG_UG2_UHCT_PressaoMinima = 13570
REG_UG2_UHCT_PressaoOleo = 12784
REG_UG2_UHCT_Pressostatos = 12782
REG_UG2_UHCT_Rodizio = 12779
REG_UG2_UHCT_RodizioDesabilitar = 12348
REG_UG2_UHCT_RodizioHabilitar = 12347
REG_UG2_UHCT_RodizioPrincipal = 13606
REG_UG2_UHCT_RodizioRetaguarda = 13607
REG_UG2_UHCT_SensorAtivar = 12345
REG_UG2_UHCT_SensorDesativar = 12346
REG_UG2_UHCT_Valvulas = 12780
REG_UG2_UHLM_AcumuladorRodizioPrincipal = 12794
REG_UG2_UHLM_AcumuladorRodizioRetaguarda = 12795
REG_UG2_UHLM_Bomba01Desligar = 12350
REG_UG2_UHLM_Bomba01Ligar = 12349
REG_UG2_UHLM_Bomba01Principal = 12351
REG_UG2_UHLM_Bomba02Desligar = 12353
REG_UG2_UHLM_Bomba02Ligar = 12352
REG_UG2_UHLM_Bomba02Principal = 12354
REG_UG2_UHLM_BombaAguaDesliga = 12358
REG_UG2_UHLM_BombaAguaLiga = 12357
REG_UG2_UHLM_BombaJackingDesliga = 12356
REG_UG2_UHLM_BombaJackingLiga = 12355
REG_UG2_UHLM_Bombas = 12788
REG_UG2_UHLM_Filtros = 12790
REG_UG2_UHLM_Fluxostatos = 12792
REG_UG2_UHLM_Info = 12787
REG_UG2_UHLM_Nivel = 12793
REG_UG2_UHLM_Pressostatos = 12791
REG_UG2_UHLM_Rodizio = 12789
REG_UG2_UHLM_RodizioDesabilitar = 12360
REG_UG2_UHLM_RodizioHabilitar = 12359
REG_UG2_UHLM_RodizioPrincipal = 13608
REG_UG2_UHLM_RodizioRetaguarda = 13609
REG_UG2_VersaoBase = 12764
REG_UG2_VersaoCustom = 12765
REG_USINA_Alarme01 = 14199
REG_USINA_Alarme02 = 14200
REG_USINA_Alarme03 = 14201
REG_USINA_Alarme04 = 14202
REG_USINA_Alarme05 = 14203
REG_USINA_Alarme06 = 14204
REG_USINA_Alarme07 = 14205
REG_USINA_Alarme08 = 14206
REG_USINA_Alarme09 = 14207
REG_USINA_Alarme10 = 14208
REG_USINA_Alarme11 = 14209
REG_USINA_Alarme12 = 14210
REG_USINA_Alarme13 = 14211
REG_USINA_Alarme14 = 14212
REG_USINA_Alarme15 = 14213
REG_USINA_Alarme16 = 14214
REG_USINA_CB_CorrenteBaterias = 12979
REG_USINA_CB_CorrenteConsumidor = 12977
REG_USINA_CB_CorrenteFugaTerra = 12982
REG_USINA_CB_CorrenteRetificador = 12981
REG_USINA_CB_TempBaterias = 12975
REG_USINA_CB_TempInterna = 12974
REG_USINA_CB_TensaoBaterias = 12978
REG_USINA_CB_TensaoConsumidor = 12976
REG_USINA_CB_TensaoRetificador = 12980
REG_USINA_CarregadorBateria_IEntrada = 12777
REG_USINA_CarregadorBateria_ISaida = 12778
REG_USINA_CarregadorBateria_Info = 12774
REG_USINA_CarregadorBateria_ModoEqualizacaoLigar = 12308
REG_USINA_CarregadorBateria_ModoFlutuacaoLigar = 12307
REG_USINA_CarregadorBateria_UEntrada = 12775
REG_USINA_CarregadorBateria_USaida = 12776
REG_USINA_Comporta_Referencia1 = 13640
REG_USINA_Comporta_Referencia2 = 13641
REG_USINA_Comporta_Referencia3 = 13642
REG_USINA_Comporta_Referencia4 = 13643
REG_USINA_Comporta_Referencia5 = 13644
REG_USINA_CtrlPotencia_ModoNivelDesligar = 12341
REG_USINA_CtrlPotencia_ModoNivelLigar = 12340
REG_USINA_CtrlPotencia_N00_ds = 13592
REG_USINA_CtrlPotencia_N00_fds = 13616
REG_USINA_CtrlPotencia_N01_ds = 13593
REG_USINA_CtrlPotencia_N01_fds = 13617
REG_USINA_CtrlPotencia_N02_ds = 13594
REG_USINA_CtrlPotencia_N02_fds = 13618
REG_USINA_CtrlPotencia_N03_ds = 13595
REG_USINA_CtrlPotencia_N03_fds = 13619
REG_USINA_CtrlPotencia_N04_ds = 13596
REG_USINA_CtrlPotencia_N04_fds = 13620
REG_USINA_CtrlPotencia_N05_ds = 13597
REG_USINA_CtrlPotencia_N05_fds = 13621
REG_USINA_CtrlPotencia_N06_ds = 13598
REG_USINA_CtrlPotencia_N06_fds = 13622
REG_USINA_CtrlPotencia_N07_ds = 13599
REG_USINA_CtrlPotencia_N07_fds = 13623
REG_USINA_CtrlPotencia_N08_ds = 13600
REG_USINA_CtrlPotencia_N08_fds = 13624
REG_USINA_CtrlPotencia_N09_ds = 13601
REG_USINA_CtrlPotencia_N09_fds = 13625
REG_USINA_CtrlPotencia_N10_ds = 13602
REG_USINA_CtrlPotencia_N10_fds = 13626
REG_USINA_CtrlPotencia_N11_ds = 13603
REG_USINA_CtrlPotencia_N11_fds = 13627
REG_USINA_CtrlPotencia_N12_ds = 13604
REG_USINA_CtrlPotencia_N12_fds = 13628
REG_USINA_CtrlPotencia_N13_ds = 13605
REG_USINA_CtrlPotencia_N13_fds = 13629
REG_USINA_CtrlPotencia_N14_ds = 13606
REG_USINA_CtrlPotencia_N14_fds = 13630
REG_USINA_CtrlPotencia_N15_ds = 13607
REG_USINA_CtrlPotencia_N15_fds = 13631
REG_USINA_CtrlPotencia_N16_ds = 13608
REG_USINA_CtrlPotencia_N16_fds = 13632
REG_USINA_CtrlPotencia_N17_ds = 13609
REG_USINA_CtrlPotencia_N17_fds = 13633
REG_USINA_CtrlPotencia_N18_ds = 13610
REG_USINA_CtrlPotencia_N18_fds = 13634
REG_USINA_CtrlPotencia_N19_ds = 13611
REG_USINA_CtrlPotencia_N19_fds = 13635
REG_USINA_CtrlPotencia_N20_ds = 13612
REG_USINA_CtrlPotencia_N20_fds = 13636
REG_USINA_CtrlPotencia_N21_ds = 13613
REG_USINA_CtrlPotencia_N21_fds = 13637
REG_USINA_CtrlPotencia_N22_ds = 13614
REG_USINA_CtrlPotencia_N22_fds = 13638
REG_USINA_CtrlPotencia_N23_ds = 13615
REG_USINA_CtrlPotencia_N23_fds = 13639
REG_USINA_CtrlPotencia_NivelDesligamento = 13591
REG_USINA_CtrlPotencia_NivelReligamento = 13590
REG_USINA_CtrlPotencia_PotenciaMaxima = 13586
REG_USINA_CtrlPotencia_PotenciaMinima = 13585
REG_USINA_CtrlPotencia_PulsoIntervalo = 13588
REG_USINA_CtrlPotencia_PulsoPotencia = 13587
REG_USINA_CtrlPotencia_ReligamentoDesligar = 12339
REG_USINA_CtrlPotencia_ReligamentoLigar = 12338
REG_USINA_CtrlPotencia_SetpointNivel = 13584
REG_USINA_CtrlPotencia_Tolerancia = 13589
REG_USINA_Disj52LAbrir = 12293
REG_USINA_Disj52LFechar = 12294
REG_USINA_Disjuntor_01 = 12564
REG_USINA_Disjuntor_02 = 12565
REG_USINA_Disjuntor_03 = 12566
REG_USINA_Disjuntor_04 = 12567
REG_USINA_Disjuntor_05 = 12568
REG_USINA_Disjuntor_06 = 12569
REG_USINA_Disjuntor_07 = 12570
REG_USINA_Disjuntor_08 = 12571
REG_USINA_Disjuntor_09 = 12572
REG_USINA_Disjuntor_10 = 12573
REG_USINA_Disjuntor_11 = 12574
REG_USINA_Disjuntor_12 = 12575
REG_USINA_Disjuntor_13 = 12576
REG_USINA_Disjuntor_14 = 12577
REG_USINA_Disjuntor_15 = 12578
REG_USINA_Disjuntor_16 = 12579
REG_USINA_Disjuntor_17 = 12580
REG_USINA_Disjuntor_18 = 12581
REG_USINA_Disjuntor_19 = 12582
REG_USINA_Disjuntor_20 = 12583
REG_USINA_Disjuntor_21 = 12584
REG_USINA_Disjuntor_22 = 12585
REG_USINA_Disjuntor_23 = 12586
REG_USINA_Disjuntor_24 = 12587
REG_USINA_Disjuntor_25 = 12588
REG_USINA_Disjuntor_26 = 12589
REG_USINA_Disjuntor_27 = 12590
REG_USINA_Disjuntor_28 = 12591
REG_USINA_Disjuntor_29 = 12592
REG_USINA_Disjuntor_30 = 12593
REG_USINA_Disjuntor_31 = 12594
REG_USINA_Disjuntor_32 = 12595
REG_USINA_Disjuntor_33 = 12596
REG_USINA_Disjuntor_34 = 12597
REG_USINA_Disjuntor_35 = 12598
REG_USINA_Disjuntor_36 = 12599
REG_USINA_Disjuntor_37 = 12600
REG_USINA_Disjuntor_38 = 12601
REG_USINA_Disjuntor_39 = 12602
REG_USINA_Disjuntor_40 = 12603
REG_USINA_Disjuntor_41 = 12604
REG_USINA_Disjuntor_42 = 12605
REG_USINA_Disjuntor_43 = 12606
REG_USINA_Disjuntor_44 = 12607
REG_USINA_Disjuntor_45 = 12608
REG_USINA_Disjuntor_46 = 12609
REG_USINA_Disjuntor_47 = 12610
REG_USINA_Disjuntor_48 = 12611
REG_USINA_Disjuntor_49 = 12612
REG_USINA_Disjuntor_50 = 12613
REG_USINA_Disjuntor_51 = 12614
REG_USINA_Disjuntor_52 = 12615
REG_USINA_Disjuntor_53 = 12616
REG_USINA_Disjuntor_54 = 12617
REG_USINA_Disjuntor_55 = 12618
REG_USINA_Disjuntor_56 = 12619
REG_USINA_Disjuntor_57 = 12620
REG_USINA_Disjuntor_58 = 12621
REG_USINA_Disjuntor_59 = 12622
REG_USINA_Disjuntor_60 = 12623
REG_USINA_Disjuntor_61 = 12624
REG_USINA_Disjuntor_62 = 12625
REG_USINA_Disjuntor_63 = 12626
REG_USINA_Disjuntor_64 = 12627
REG_USINA_EA00_amostragem = 14285
REG_USINA_EA00_intervalo = 14284
REG_USINA_EA00_offset = 14283
REG_USINA_EA00_x = 14286
REG_USINA_EA00_x0 = 14279
REG_USINA_EA00_x1 = 14280
REG_USINA_EA00_y0 = 14281
REG_USINA_EA00_y1 = 14282
REG_USINA_EA01_amostragem = 14293
REG_USINA_EA01_intervalo = 14292
REG_USINA_EA01_offset = 14291
REG_USINA_EA01_x = 14294
REG_USINA_EA01_x0 = 14287
REG_USINA_EA01_x1 = 14288
REG_USINA_EA01_y0 = 14289
REG_USINA_EA01_y1 = 14290
REG_USINA_EA02_amostragem = 14301
REG_USINA_EA02_intervalo = 14300
REG_USINA_EA02_offset = 14299
REG_USINA_EA02_x = 14302
REG_USINA_EA02_x0 = 14295
REG_USINA_EA02_x1 = 14296
REG_USINA_EA02_y0 = 14297
REG_USINA_EA02_y1 = 14298
REG_USINA_EA03_amostragem = 14309
REG_USINA_EA03_intervalo = 14308
REG_USINA_EA03_offset = 14307
REG_USINA_EA03_x = 14310
REG_USINA_EA03_x0 = 14303
REG_USINA_EA03_x1 = 14304
REG_USINA_EA03_y0 = 14305
REG_USINA_EA03_y1 = 14306
REG_USINA_EA04_amostragem = 14317
REG_USINA_EA04_intervalo = 14316
REG_USINA_EA04_offset = 14315
REG_USINA_EA04_x = 14318
REG_USINA_EA04_x0 = 14311
REG_USINA_EA04_x1 = 14312
REG_USINA_EA04_y0 = 14313
REG_USINA_EA04_y1 = 14314
REG_USINA_EA05_amostragem = 14325
REG_USINA_EA05_intervalo = 14324
REG_USINA_EA05_offset = 14323
REG_USINA_EA05_x = 14326
REG_USINA_EA05_x0 = 14319
REG_USINA_EA05_x1 = 14320
REG_USINA_EA05_y0 = 14321
REG_USINA_EA05_y1 = 14322
REG_USINA_EA06_amostragem = 14333
REG_USINA_EA06_intervalo = 14332
REG_USINA_EA06_offset = 14331
REG_USINA_EA06_x = 14334
REG_USINA_EA06_x0 = 14327
REG_USINA_EA06_x1 = 14328
REG_USINA_EA06_y0 = 14329
REG_USINA_EA06_y1 = 14330
REG_USINA_EA07_amostragem = 14341
REG_USINA_EA07_intervalo = 14340
REG_USINA_EA07_offset = 14339
REG_USINA_EA07_x = 14342
REG_USINA_EA07_x0 = 14335
REG_USINA_EA07_x1 = 14336
REG_USINA_EA07_y0 = 14337
REG_USINA_EA07_y1 = 14338
REG_USINA_EA08_amostragem = 14349
REG_USINA_EA08_intervalo = 14348
REG_USINA_EA08_offset = 14347
REG_USINA_EA08_x = 14350
REG_USINA_EA08_x0 = 14343
REG_USINA_EA08_x1 = 14344
REG_USINA_EA08_y0 = 14345
REG_USINA_EA08_y1 = 14346
REG_USINA_EA09_amostragem = 14357
REG_USINA_EA09_intervalo = 14356
REG_USINA_EA09_offset = 14355
REG_USINA_EA09_x = 14358
REG_USINA_EA09_x0 = 14351
REG_USINA_EA09_x1 = 14352
REG_USINA_EA09_y0 = 14353
REG_USINA_EA09_y1 = 14354
REG_USINA_EA10_amostragem = 14365
REG_USINA_EA10_intervalo = 14364
REG_USINA_EA10_offset = 14363
REG_USINA_EA10_x = 14366
REG_USINA_EA10_x0 = 14359
REG_USINA_EA10_x1 = 14360
REG_USINA_EA10_y0 = 14361
REG_USINA_EA10_y1 = 14362
REG_USINA_EA11_amostragem = 14373
REG_USINA_EA11_intervalo = 14372
REG_USINA_EA11_offset = 14371
REG_USINA_EA11_x = 14374
REG_USINA_EA11_x0 = 14367
REG_USINA_EA11_x1 = 14368
REG_USINA_EA11_y0 = 14369
REG_USINA_EA11_y1 = 14370
REG_USINA_EA12_amostragem = 14381
REG_USINA_EA12_intervalo = 14380
REG_USINA_EA12_offset = 14379
REG_USINA_EA12_x = 14382
REG_USINA_EA12_x0 = 14375
REG_USINA_EA12_x1 = 14376
REG_USINA_EA12_y0 = 14377
REG_USINA_EA12_y1 = 14378
REG_USINA_EA13_amostragem = 14389
REG_USINA_EA13_intervalo = 14388
REG_USINA_EA13_offset = 14387
REG_USINA_EA13_x = 14390
REG_USINA_EA13_x0 = 14383
REG_USINA_EA13_x1 = 14384
REG_USINA_EA13_y0 = 14385
REG_USINA_EA13_y1 = 14386
REG_USINA_EA14_amostragem = 14397
REG_USINA_EA14_intervalo = 14396
REG_USINA_EA14_offset = 14395
REG_USINA_EA14_x = 14398
REG_USINA_EA14_x0 = 14391
REG_USINA_EA14_x1 = 14392
REG_USINA_EA14_y0 = 14393
REG_USINA_EA14_y1 = 14394
REG_USINA_EA15_amostragem = 14405
REG_USINA_EA15_intervalo = 14404
REG_USINA_EA15_offset = 14403
REG_USINA_EA15_x = 14406
REG_USINA_EA15_x0 = 14399
REG_USINA_EA15_x1 = 14400
REG_USINA_EA15_y0 = 14401
REG_USINA_EA15_y1 = 14402
REG_USINA_EmergenciaDesligar = 12292
REG_USINA_EmergenciaLigar = 12291
REG_USINA_GeradorDiesel_CorrenteMedia = 12940
REG_USINA_GeradorDiesel_CorrenteR = 12937
REG_USINA_GeradorDiesel_CorrenteS = 12938
REG_USINA_GeradorDiesel_CorrenteT = 12939
REG_USINA_GeradorDiesel_EnergiaConsumidaAtivaGWh = 12958
REG_USINA_GeradorDiesel_EnergiaConsumidaAtivaMWh = 12959
REG_USINA_GeradorDiesel_EnergiaConsumidaAtivaWh = 12961
REG_USINA_GeradorDiesel_EnergiaConsumidaAtivakWh = 12960
REG_USINA_GeradorDiesel_EnergiaConsumidaReativaGvarh = 12962
REG_USINA_GeradorDiesel_EnergiaConsumidaReativaMvarh = 12963
REG_USINA_GeradorDiesel_EnergiaConsumidaReativakvarh = 12964
REG_USINA_GeradorDiesel_EnergiaConsumidaReativavarh = 12965
REG_USINA_GeradorDiesel_EnergiaFornecidaReativaGvarh = 12966
REG_USINA_GeradorDiesel_EnergiaFornecidaReativaMvarh = 12967
REG_USINA_GeradorDiesel_EnergiaFornecidaReativakvarh = 12968
REG_USINA_GeradorDiesel_EnergiaFornecidaReativavarh = 12969
REG_USINA_GeradorDiesel_FP_Info = 12970
REG_USINA_GeradorDiesel_FatorPotencia1 = 12953
REG_USINA_GeradorDiesel_FatorPotencia2 = 12954
REG_USINA_GeradorDiesel_FatorPotencia3 = 12955
REG_USINA_GeradorDiesel_FatorPotenciaMedia = 12956
REG_USINA_GeradorDiesel_Frequencia = 12957
REG_USINA_GeradorDiesel_PotenciaAparente1 = 12949
REG_USINA_GeradorDiesel_PotenciaAparente2 = 12950
REG_USINA_GeradorDiesel_PotenciaAparente3 = 12951
REG_USINA_GeradorDiesel_PotenciaAparenteTotal = 12952
REG_USINA_GeradorDiesel_PotenciaAtiva1 = 12941
REG_USINA_GeradorDiesel_PotenciaAtiva2 = 12942
REG_USINA_GeradorDiesel_PotenciaAtiva3 = 12943
REG_USINA_GeradorDiesel_PotenciaAtivaTotal = 12944
REG_USINA_GeradorDiesel_PotenciaReativa1 = 12945
REG_USINA_GeradorDiesel_PotenciaReativa2 = 12946
REG_USINA_GeradorDiesel_PotenciaReativa3 = 12947
REG_USINA_GeradorDiesel_PotenciaReativaTotal = 12948
REG_USINA_GeradorDiesel_TensaoRN = 12931
REG_USINA_GeradorDiesel_TensaoRS = 12934
REG_USINA_GeradorDiesel_TensaoSN = 12932
REG_USINA_GeradorDiesel_TensaoST = 12935
REG_USINA_GeradorDiesel_TensaoTN = 12933
REG_USINA_GeradorDiesel_TensaoTR = 12936
REG_USINA_GrupoDiesel_Info = 12779
REG_USINA_GrupoDiesel_NivelCombustivel = 12780
REG_USINA_GrupoDiesel_Parar = 12306
REG_USINA_GrupoDiesel_Partir = 12305
REG_USINA_GrupoDiesel_RotacaoMotor = 12781
REG_USINA_GrupoDiesel_TensaoAlternador = 12783
REG_USINA_GrupoDiesel_TensaoBateria = 12782
REG_USINA_ModoLocal = 12336
REG_USINA_ModoRemoto = 12337
REG_USINA_NivelBarragem = 12767
REG_USINA_NivelBarragem = 12767
REG_USINA_NivelCamaraCarga = 12769
REG_USINA_NivelCamaraCarga = 12769
REG_USINA_NivelCanal = 12768
REG_USINA_NivelCanalAducao = 12768
REG_USINA_NivelJusante = 12766
REG_USINA_NivelJusante = 12766
REG_USINA_PainelReconheceAlarmes = 12771
REG_USINA_PainelResetAlarmes = 12770
REG_USINA_Pluviometro = 12773
REG_USINA_Poco_Bomba01Desligar = 12310
REG_USINA_Poco_Bomba01Ligar = 12309
REG_USINA_Poco_Bomba01Principal = 12311
REG_USINA_Poco_Bomba02Desligar = 12313
REG_USINA_Poco_Bomba02Ligar = 12312
REG_USINA_Poco_Bomba02Principal = 12314
REG_USINA_Poco_Bomba03Desligar = 12316
REG_USINA_Poco_Bomba03ligar = 12315
REG_USINA_Poco_Bomba04Desligar = 12318
REG_USINA_Poco_Bomba04ligar = 12317
REG_USINA_Poco_Bombas = 12876
REG_USINA_Poco_HorimetroPrincipal = 12878
REG_USINA_Poco_HorimetroRetaguarda = 12879
REG_USINA_Poco_Info = 12875
REG_USINA_Poco_Nivel = 12877
REG_USINA_Poco_SelecionaModoAutomatico = 12320
REG_USINA_Poco_SelecionaModoManual = 12319
REG_USINA_Poco_TempoRodizioLider = 13577
REG_USINA_Poco_TempoRodizioRetaguarda = 13578
REG_USINA_PressaoArComprimido = 12983
REG_USINA_PressaoBaixaArComprimido = 13645
REG_USINA_QCTA_Bomba01Desligar = 12327
REG_USINA_QCTA_Bomba01Ligar = 12326
REG_USINA_QCTA_Bomba01Principal = 12328
REG_USINA_QCTA_Bomba02Desligar = 12330
REG_USINA_QCTA_Bomba02Ligar = 12329
REG_USINA_QCTA_Bomba02Principal = 12331
REG_USINA_QCTA_ComportaInfo = 682 + 12288
REG_USINA_QCTA_ComportaAbrir = 12323
REG_USINA_QCTA_ComportaFechar = 12325
REG_USINA_QCTA_ComportaParar = 12324
REG_USINA_QCTA_ModoAutomatico = 12333
REG_USINA_QCTA_ModoManual = 12332
REG_USINA_QCTA_NivelReferencia = 13581
REG_USINA_QCTA_NivelTolerancia = 13582
REG_USINA_QCTA_NivelVerificacao = 13583
REG_USINA_QCTA_RodizioAutomatico = 12334
REG_USINA_QCTA_RodizioLider = 13579
REG_USINA_QCTA_RodizioManual = 12335
REG_USINA_QCTA_RodizioRetaguarda = 13580
REG_USINA_QCTA_UHTA_Comporta = 12971
REG_USINA_QCTA_UHTA_Info = 12972
REG_USINA_QCTA_UHTA_Temperatura = 12973
REG_USINA_ReconheceAlarmes = 12290
REG_USINA_ResetAlarmes = 12289
REG_USINA_SGI_Info = 12882
REG_USINA_SensorFumaca_Info = 12880
REG_USINA_SensorPresenca_Desabilitar = 12322
REG_USINA_SensorPresenca_Habilitar = 12321
REG_USINA_SensorPresenca_Info = 12881
REG_USINA_ServAux_FPInfo = 12873
REG_USINA_ServAux_FugaTerra_Info = 12874
REG_USINA_ServAux_FugaTerra_Tensao = 12872
REG_USINA_ServAux_FugaTerra_TensaoNegativa = 12871
REG_USINA_ServAux_FugaTerra_TensaoPositiva = 12870
REG_USINA_ServAuxiliar_CorrenteMedia = 12840
REG_USINA_ServAuxiliar_CorrenteR = 12837
REG_USINA_ServAuxiliar_CorrenteS = 12838
REG_USINA_ServAuxiliar_CorrenteT = 12839
REG_USINA_ServAuxiliar_DisjFonte01Desligar = 12300
REG_USINA_ServAuxiliar_DisjFonte01Ligar = 12299
REG_USINA_ServAuxiliar_DisjFonte02Desligar = 12302
REG_USINA_ServAuxiliar_DisjFonte02Ligar = 12301
REG_USINA_ServAuxiliar_DisjFonte03Desligar = 12304
REG_USINA_ServAuxiliar_DisjFonte03Ligar = 12303
REG_USINA_ServAuxiliar_EnergiaConsumidaGVArh = 12862
REG_USINA_ServAuxiliar_EnergiaConsumidaGWh = 12858
REG_USINA_ServAuxiliar_EnergiaConsumidaKVArh = 12864
REG_USINA_ServAuxiliar_EnergiaConsumidaKWh = 12860
REG_USINA_ServAuxiliar_EnergiaConsumidaMVArh = 12863
REG_USINA_ServAuxiliar_EnergiaConsumidaMWh = 12859
REG_USINA_ServAuxiliar_EnergiaConsumidaWVArh = 12865
REG_USINA_ServAuxiliar_EnergiaConsumidaWh = 12861
REG_USINA_ServAuxiliar_EnergiaFornecidaGVArh = 12866
REG_USINA_ServAuxiliar_EnergiaFornecidaKVArh = 12868
REG_USINA_ServAuxiliar_EnergiaFornecidaMVArh = 12867
REG_USINA_ServAuxiliar_EnergiaFornecidaVArh = 12869
REG_USINA_ServAuxiliar_FatorPotencia1 = 12853
REG_USINA_ServAuxiliar_FatorPotencia2 = 12854
REG_USINA_ServAuxiliar_FatorPotencia3 = 12855
REG_USINA_ServAuxiliar_FatorPotenciaMedia = 12856
REG_USINA_ServAuxiliar_Frequencia = 12857
REG_USINA_ServAuxiliar_Info = 12830
REG_USINA_ServAuxiliar_PotenciaAparente1 = 12849
REG_USINA_ServAuxiliar_PotenciaAparente2 = 12850
REG_USINA_ServAuxiliar_PotenciaAparente3 = 12851
REG_USINA_ServAuxiliar_PotenciaAparenteMedia = 12852
REG_USINA_ServAuxiliar_PotenciaAtiva1 = 12841
REG_USINA_ServAuxiliar_PotenciaAtiva2 = 12842
REG_USINA_ServAuxiliar_PotenciaAtiva3 = 12843
REG_USINA_ServAuxiliar_PotenciaAtivaMedia = 12844
REG_USINA_ServAuxiliar_PotenciaReativa1 = 12845
REG_USINA_ServAuxiliar_PotenciaReativa2 = 12846
REG_USINA_ServAuxiliar_PotenciaReativa3 = 12847
REG_USINA_ServAuxiliar_PotenciaReativaMedia = 12848
REG_USINA_ServAuxiliar_SelecionaModoAutomatico = 12298
REG_USINA_ServAuxiliar_SelecionaModoLocal = 12295
REG_USINA_ServAuxiliar_SelecionaModoManual = 12297
REG_USINA_ServAuxiliar_SelecionaModoRemoto = 12296
REG_USINA_ServAuxiliar_TensaoRN = 12831
REG_USINA_ServAuxiliar_TensaoRS = 12834
REG_USINA_ServAuxiliar_TensaoSN = 12832
REG_USINA_ServAuxiliar_TensaoST = 12835
REG_USINA_ServAuxiliar_TensaoTN = 12833
REG_USINA_ServAuxiliar_TensaoTR = 12836
REG_USINA_Subestacao_CorrenteMedia = 12796
REG_USINA_Subestacao_CorrenteNeutro = 12826
REG_USINA_Subestacao_CorrenteR = 12793
REG_USINA_Subestacao_CorrenteS = 12794
REG_USINA_Subestacao_CorrenteT = 12795
REG_USINA_Subestacao_Disj52L = 12785
REG_USINA_Subestacao_EnergiaConsumidaGVArh = 12823
REG_USINA_Subestacao_EnergiaConsumidaKVArh = 12825
REG_USINA_Subestacao_EnergiaConsumidaMVArh = 12824
REG_USINA_Subestacao_EnergiaConsumidaTVArh = 12822
REG_USINA_Subestacao_EnergiaFornecidaGVArh = 12819
REG_USINA_Subestacao_EnergiaFornecidaGWh = 12815
REG_USINA_Subestacao_EnergiaFornecidaKVArh = 12821
REG_USINA_Subestacao_EnergiaFornecidaKWh = 12817
REG_USINA_Subestacao_EnergiaFornecidaMVArh = 12820
REG_USINA_Subestacao_EnergiaFornecidaMWh = 12816
REG_USINA_Subestacao_EnergiaFornecidaTVArh = 12818
REG_USINA_Subestacao_EnergiaFornecidaTWh = 12814
REG_USINA_Subestacao_FPInfo = 12829
REG_USINA_Subestacao_FatorPotencia1 = 12809
REG_USINA_Subestacao_FatorPotencia2 = 12810
REG_USINA_Subestacao_FatorPotencia3 = 12811
REG_USINA_Subestacao_FatorPotenciaMedia = 12812
REG_USINA_Subestacao_Frequencia = 12813
REG_USINA_Subestacao_PotenciaAparente1 = 12805
REG_USINA_Subestacao_PotenciaAparente2 = 12806
REG_USINA_Subestacao_PotenciaAparente3 = 12807
REG_USINA_Subestacao_PotenciaAparenteMedia = 12808
REG_USINA_Subestacao_PotenciaAtiva1 = 12797
REG_USINA_Subestacao_PotenciaAtiva2 = 12798
REG_USINA_Subestacao_PotenciaAtiva3 = 12799
REG_USINA_Subestacao_PotenciaAtivaMedia = 12800
REG_USINA_Subestacao_PotenciaReativa1 = 12801
REG_USINA_Subestacao_PotenciaReativa2 = 12802
REG_USINA_Subestacao_PotenciaReativa3 = 12803
REG_USINA_Subestacao_PotenciaReativaMedia = 12804
REG_USINA_Subestacao_Seccionadoras = 12786
REG_USINA_Subestacao_TensaoRN = 12787
REG_USINA_Subestacao_TensaoRS = 12790
REG_USINA_Subestacao_TensaoSN = 12788
REG_USINA_Subestacao_TensaoST = 12791
REG_USINA_Subestacao_TensaoSincronismo = 12827
REG_USINA_Subestacao_TensaoTN = 12789
REG_USINA_Subestacao_TensaoTR = 12792
REG_USINA_Subestacao_TensaoVCC = 12828
REG_USINA_TrafoAuxiliar_CorrenteMedia = 12900
REG_USINA_TrafoAuxiliar_CorrenteR = 12897
REG_USINA_TrafoAuxiliar_CorrenteS = 12898
REG_USINA_TrafoAuxiliar_CorrenteT = 12899
REG_USINA_TrafoAuxiliar_EnergiaConsumidaAtivaGWh = 12918
REG_USINA_TrafoAuxiliar_EnergiaConsumidaAtivaMWh = 12919
REG_USINA_TrafoAuxiliar_EnergiaConsumidaAtivaWh = 12921
REG_USINA_TrafoAuxiliar_EnergiaConsumidaAtivakWh = 12920
REG_USINA_TrafoAuxiliar_EnergiaConsumidaReativaGvarh = 12922
REG_USINA_TrafoAuxiliar_EnergiaConsumidaReativaMvarh = 12923
REG_USINA_TrafoAuxiliar_EnergiaConsumidaReativakvarh = 12924
REG_USINA_TrafoAuxiliar_EnergiaConsumidaReativavarh = 12925
REG_USINA_TrafoAuxiliar_EnergiaFornecidaReativaGvarh = 12926
REG_USINA_TrafoAuxiliar_EnergiaFornecidaReativaMvarh = 12927
REG_USINA_TrafoAuxiliar_EnergiaFornecidaReativakvarh = 12928
REG_USINA_TrafoAuxiliar_EnergiaFornecidaReativavarh = 12929
REG_USINA_TrafoAuxiliar_FP_Info = 12930
REG_USINA_TrafoAuxiliar_FatorPotencia1 = 12913
REG_USINA_TrafoAuxiliar_FatorPotencia2 = 12914
REG_USINA_TrafoAuxiliar_FatorPotencia3 = 12915
REG_USINA_TrafoAuxiliar_FatorPotenciaMedia = 12916
REG_USINA_TrafoAuxiliar_Frequencia = 12917
REG_USINA_TrafoAuxiliar_PotenciaAparente1 = 12909
REG_USINA_TrafoAuxiliar_PotenciaAparente2 = 12910
REG_USINA_TrafoAuxiliar_PotenciaAparente3 = 12911
REG_USINA_TrafoAuxiliar_PotenciaAparenteTotal = 12912
REG_USINA_TrafoAuxiliar_PotenciaAtiva1 = 12901
REG_USINA_TrafoAuxiliar_PotenciaAtiva2 = 12902
REG_USINA_TrafoAuxiliar_PotenciaAtiva3 = 12903
REG_USINA_TrafoAuxiliar_PotenciaAtivaTotal = 12904
REG_USINA_TrafoAuxiliar_PotenciaReativa1 = 12905
REG_USINA_TrafoAuxiliar_PotenciaReativa2 = 12906
REG_USINA_TrafoAuxiliar_PotenciaReativa3 = 12907
REG_USINA_TrafoAuxiliar_PotenciaReativaTotal = 12908
REG_USINA_TrafoAuxiliar_TensaoRN = 12891
REG_USINA_TrafoAuxiliar_TensaoRS = 12894
REG_USINA_TrafoAuxiliar_TensaoSN = 12892
REG_USINA_TrafoAuxiliar_TensaoST = 12895
REG_USINA_TrafoAuxiliar_TensaoTN = 12893
REG_USINA_TrafoAuxiliar_TensaoTR = 12896
REG_USINA_TrafoElevador_Info = 12784
REG_USINA_Usina_Emergencia_Info = 12772
REG_USINA_Usina_GradeSujaDiferencial_Alarme = 13575
REG_USINA_Usina_GradeSujaDiferencial_TRIP = 13576
REG_USINA_Usina_NiveCamaraCarga_HH = 13572
REG_USINA_Usina_NiveCamaraCarga_LL = 13573
REG_USINA_Usina_NiveCamaraCarga_Tolerancia = 13574
REG_USINA_Usina_NivelBarragem_HH = 13569
REG_USINA_Usina_NivelBarragem_LL = 13570
REG_USINA_Usina_NivelBarragem_Tolerancia = 13571
REG_USINA_Usina_Temperatura_01 = 12883
REG_USINA_Usina_Temperatura_02 = 12884
REG_USINA_Usina_Temperatura_03 = 12885
REG_USINA_Usina_Temperatura_04 = 12886
REG_USINA_Usina_Temperatura_05 = 12887
REG_USINA_Usina_Temperatura_06 = 12888
REG_USINA_Usina_Temperatura_07 = 12889
REG_USINA_Usina_Temperatura_08 = 12890
REG_USINA_VersaoBase = 12764
REG_USINA_VersaoCustom = 12765   