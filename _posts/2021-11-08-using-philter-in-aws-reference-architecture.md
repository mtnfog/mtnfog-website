---
date: 2021-11-08
title: Using Philter in the AWS Reference Architecture for HIPAA
layout: post
categories:
  - philter
  - aws
---

AWS has provided a HIPAA Reference Architecture for applications that contain protected health information (PHI). This reference architecture gives us a starting point for a highly-available architecture that spans multiple availability zones, three VPCs for management, production, and development resources, logging, VPN for customer connectivity, along with a set of AWS config rules and logging. The source code for the reference architecture is available.

<a href="/philter">Philter</a> is our software that redacts PHI, PII, and other sensitive information from text and documents. Philter runs in your cloud so your data never leaves your network to be redacted and its API allows for integration into virtually any application or system. In this blog post we will look at how Philter can be deployed via the AWS Marketplace inside an architecture developed using the AWS HIPAA Reference Architecture.

## AWS Reference Architecture for HIPAA with Philter

The image below shows the AWS Reference Architecture for HIPAA with Philter deployments.

<a href="/images/blog/hipaa-aws-architecture.png" data-lightbox="image-1" data-title="AWS Reference Architecture for HIPAA with Philter deployment">
<img src="/images/blog/hipaa-aws-architecture.png" title="HIPAA Reference Architecture with Philter" data-lightbox="image-1" data-title="AWS Reference Architecture for HIPAA with Philter deployment">
</a>

## Redacting PHI in your application
Your application has the requirement of redacting PHI prior to processing and you want to deploy Philter in this reference architecture. So how does Philter fit into this architecture? The answer is seamlessly. Philter can be deployed from the AWS Marketplace into one of the private subnets in the production VPC. From there, Philter’s API will be available to the rest of your application. Your application can now send data to Philter for redaction and receive back the redacted text. The VPC flow logs configured as part of the reference architecture will capture the network traffic and Philter’s application and system log can be sent to CloudWatch Logs.

If you want to customize the configuration of Philter you can create an AMI from the Philter AMI on the AWS Marketplace. This may be useful if you want to “bake in” configuration for sending logs to CloudWatch Logs or an organizational SSL certificate.

## Highly-available Philter deployment
For a highly available Philter deployment, create an autoscaling group for the Philter AMI in the two private subnets of the production VPC. Create a load balancer in the production VPC and register the autoscaling group with it. Now, you have a single endpoint for Philter’s API with a load balanced, highly-available set of instances behind the load balancer. You can configure auto scaling policies if you would like the Philter instances to scale up or down based on network traffic (or some other metric).

## Data encryption
Network traffic to Philter will be encrypted. By default Philter uses a self-signed certificate but you can replace it with a certificate for your organization. Also, when deploying the Philter instances be sure to do so using encrypted EBS volumes. These two items will give you encryption of data at rest and in motion for your Philter instances.

## Development
You will also want to deploy an instance of Philter in the private subnet of the development VPC. This will give you an instance of Philter to use while developing and testing your application. This Philter instance can be a smaller instance type, such as a t3.large, to save cost.

## Get started
To get started, visit Philter from the <a href="{{ site.links_philter_aws }}">AWS Marketplace</a>.