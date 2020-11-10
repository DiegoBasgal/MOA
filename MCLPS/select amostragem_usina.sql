-- Sleciona os dados necessários para reproduzir o comportamento da usina no MCLPS
SELECT [E3TimeStamp]
      ,[nivel_montante]
      ,[potencia_ug1]
      ,[energia_ug1]
      ,[potencia_ug2]
      ,[energia_ug2]
      ,[comporta_value]
      ,[comporta_fechada]
      ,[comporta_pos_1]
      ,[comporta_pos_2]
      ,[comporta_pos_3]
      ,[comporta_pos_4]
      ,[comporta_aberta]
FROM [CLP].[dbo].[amostragem_usina]
ORDER BY E3TimeStamp ASC