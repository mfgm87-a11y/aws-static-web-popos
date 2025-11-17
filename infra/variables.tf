variable "aws_region" {
  description = "Región de AWS a usar"
  type        = string
  default     = "us-east-1"
}

variable "website_bucket_name" {
  description = "Nombre del bucket S3 para el sitio estático (debe ser único en S3)"
  type        = string
  default     = "aws-static-web-popos"
}
