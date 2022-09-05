CREATE EXTERNAL TABLE IF NOT EXISTS `evaluation_store_table`.`my_ingested_data` (
  `change` int,
  `ticker_symbol` string,
  `sector` string
)
ROW FORMAT SERDE 'org.apache.hive.hcatalog.data.JsonSerDe'
WITH SERDEPROPERTIES ('serialization.format' = '1')
LOCATION 's3://addi-challenge-evaluation-store/'W
TBLPROPERTIES ('has_encrypted_data' = 'false');