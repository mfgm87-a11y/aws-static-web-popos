output "website_bucket_name" {
  description = "Nombre del bucket S3 del sitio"
  value       = aws_s3_bucket.website.id
}

output "website_endpoint" {
  description = "Endpoint público del sitio estático en S3"
  value       = aws_s3_bucket_website_configuration.website.website_endpoint
}
