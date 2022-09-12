CREATE EXTERNAL TABLE IF NOT EXISTS `evaluation_store_table`.`addi_challenge_v1` (
  `event_id` string,
  `model_name` string,
  `model_version` string,
  `features` map<string,string>,
  `created_at` string,
  `prediction` string,
  `pk`string


)
ROW FORMAT SERDE 'org.apache.hive.hcatalog.data.JsonSerDe'
WITH SERDEPROPERTIES ('serialization.format' = '1')
LOCATION 's3://addi-challenge-evaluation-store/'
TBLPROPERTIES ('has_encrypted_data' = 'false');