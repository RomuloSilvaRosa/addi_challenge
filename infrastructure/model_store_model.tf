



resource "aws_iam_role" "iam-lambda-model" {
  name = "model-role"

  assume_role_policy = <<EOF
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Action": "sts:AssumeRole",
      "Principal": {
        "Service": "lambda.amazonaws.com"
      },
      "Effect": "Allow",
      "Sid": ""
    }
  ]
}
EOF
}


resource "aws_iam_policy" "lambda_model_cloudwatch" {
  name_prefix = "lambda-policy"
  policy      = <<-EOF
{   "Version": "2012-10-17",
    "Statement": [
        {
            "Action": [
                "logs:CreateLogGroup",
                 "logs:CreateLogStream",
                 "logs:PutLogEvents"
            ],
            "Effect": "Allow",
            "Resource": "arn:aws:logs:*:*:*"
        }
    ]
} 
EOF
}

resource "aws_iam_role_policy_attachment" "lambda_model_cloudwatch" {
  role       = aws_iam_role.iam-lambda-model.name
  policy_arn = aws_iam_policy.lambda_model_cloudwatch.arn
}

resource "aws_ecr_repository" "model-ecr" {
  name                 = "model/lambda"
  image_tag_mutability = "MUTABLE"

  image_scanning_configuration {
    scan_on_push = true
  }
  provisioner "local-exec" {
    command = <<-EOT
      docker pull alpine
      aws ecr get-login-password | docker login --username AWS --password-stdin ${aws_ecr_repository.model-ecr.repository_url}
      docker tag alpine "${aws_ecr_repository.model-ecr.repository_url}:latest"
      docker push "${aws_ecr_repository.model-ecr.repository_url}:latest"
    EOT
  }
}

resource "aws_lambda_function" "model-lambda" {
  function_name = "company-showcase-model"
  image_uri     = "${aws_ecr_repository.model-ecr.repository_url}:latest"
  package_type  = "Image"
  role          = aws_iam_role.iam-lambda-model.arn
  memory_size   = 1024
  timeout       = 30 # first time
}
