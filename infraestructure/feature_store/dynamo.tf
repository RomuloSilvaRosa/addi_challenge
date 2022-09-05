resource "aws_dynamodb_table" "feature-store-credit-card-dynamodb-table" {
  name           = "feature-store-credit-card"
  hash_key       = "id"
  read_capacity  = 1
  write_capacity = 1

  attribute {
    name = "id"
    type = "N"
  }
}
