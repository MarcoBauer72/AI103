IF NOT EXISTS (SELECT * FROM sys.external_file_formats WHERE name = 'SynapseParquetFormat') 
	CREATE EXTERNAL FILE FORMAT [SynapseParquetFormat] 
	WITH ( FORMAT_TYPE = PARQUET)
GO

IF NOT EXISTS (SELECT * FROM sys.external_data_sources WHERE name = 'notasfiscaisparquet_azblobpocaidocument_dfs_core_windows_net') 
	CREATE EXTERNAL DATA SOURCE [notasfiscaisparquet_azblobpocaidocument_dfs_core_windows_net] 
	WITH (
		LOCATION = 'abfss://notasfiscaisparquet@azblobpocaidocument.dfs.core.windows.net' 
	)
GO

CREATE EXTERNAL TABLE dbo.Notas (
	[NumeroNota] nvarchar(4000),
	[ValorCofins] nvarchar(4000),
	[CodigoServico] nvarchar(4000),
	[ValorTotal] nvarchar(4000),
	[ValorPIS] nvarchar(4000),
	[ValorCSLL] nvarchar(4000),
	[ValorISS] nvarchar(4000),
	[ValorIR] nvarchar(4000)
	)
	WITH (
	LOCATION = '*.parquet',
	DATA_SOURCE = [notasfiscaisparquet_azblobpocaidocument_dfs_core_windows_net],
	FILE_FORMAT = [SynapseParquetFormat]
	)
GO


SELECT TOP 100 * FROM dbo.Notas
GO