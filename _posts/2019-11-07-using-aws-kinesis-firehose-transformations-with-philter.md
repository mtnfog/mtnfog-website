---
date: 2011-08-21
title: Using AWS Kinesis Firehose Transformations to Filter Sensitive Information from Streaming Text
layout: post
categories:
  - philter
  - java
redirect_from: /blog/aws-firehose-transformations-streaming-philter/
---

AWS Kinesis Firehose is a managed streaming service designed to take large amounts of data from one place to another. For example, you can take data from places such as CloudWatch, AWS IoT, and custom applications using the AWS SDK to places such as Amazon S3, Amazon Redshift, Amazon Elasticsearch, and others. In this post we will use S3 as the firehose's destination.

In some cases you may need to manipulate the data as it goes through the firehose to remove sensitive information. In this blog post we will show how AWS Kinesis Firehose and AWS Lambda can be used in conjunction with [Philter](https://www.mtnfog.com/philter/) to remove sensitive information (PII and PHI) from the text as it travels through the firehose.

## Prerequisites

Your must have a running instance of Philter. If you don't already have a running instance of Philter you can launch one through the AWS Marketplace or as a container. There are CloudFormation and Terraform scripts for launching a single instance of Philter or a load-balanced auto-scaled set of Philter instances.

It's not required that the instance of Philter be running in AWS but it is required that the instance of Philter be accessible from your AWS Lambda function. Running Philter and your AWS Lambda function in your own VPC allows you to communicate locally with Philter from the function.

## Setting up the AWS Kinesis Firehose Transformation

There is no need to duplicate an excellent blog post on creating a [Firehose Data Transformation with AWS Lambda](https://aws.amazon.com/blogs/compute/amazon-kinesis-firehose-data-transformation-with-aws-lambda/). Instead, refer to the linked page and substitute the Python 3 code below for the code in that blog post.

## Configuring the Firehose and the Lambda Function

To start, create an AWS Firehose and configure an AWS Lambda transformation. When creating the AWS Lambda function, select Python 3.7 and use the following code:

<!-- HTML generated using hilite.me --><div style="background: #ffffff; overflow:auto;width:auto;border:solid gray;border-width:.1em .1em .1em .8em;padding:.2em .6em;"><table><tr><td><pre style="margin: 0; line-height: 125%"> 1
2
3
4
5
6
7
8
9
10
11
12
13
14
15
16
17
18
19
20</pre></td><td><pre style="margin: 0; line-height: 125%"><span style="color: #008800; font-weight: bold">from</span> <span style="color: #0e84b5; font-weight: bold">botocore.vendored</span> <span style="color: #008800; font-weight: bold">import</span> requests
<span style="color: #008800; font-weight: bold">import</span> <span style="color: #0e84b5; font-weight: bold">base64</span>

<span style="color: #008800; font-weight: bold">def</span> <span style="color: #0066BB; font-weight: bold">handler</span>(event, context):

    output <span style="color: #333333">=</span> []

    <span style="color: #008800; font-weight: bold">for</span> record <span style="color: #000000; font-weight: bold">in</span> event[<span style="background-color: #fff0f0">&#39;records&#39;</span>]:
        payload<span style="color: #333333">=</span>base64<span style="color: #333333">.</span>b64decode(record[<span style="background-color: #fff0f0">&quot;data&quot;</span>])
        headers <span style="color: #333333">=</span> {<span style="background-color: #fff0f0">&#39;Content-type&#39;</span>: <span style="background-color: #fff0f0">&#39;text/plain&#39;</span>}
        r <span style="color: #333333">=</span> requests<span style="color: #333333">.</span>post(<span style="background-color: #fff0f0">&quot;https://PHILTER_IP:8080/api/filter&quot;</span>, verify<span style="color: #333333">=</span><span style="color: #007020">False</span>, data<span style="color: #333333">=</span>payload, headers<span style="color: #333333">=</span>headers, timeout<span style="color: #333333">=</span><span style="color: #0000DD; font-weight: bold">20</span>)
        filtered <span style="color: #333333">=</span> r<span style="color: #333333">.</span>text
        output_record <span style="color: #333333">=</span> {
            <span style="background-color: #fff0f0">&#39;recordId&#39;</span>: record[<span style="background-color: #fff0f0">&#39;recordId&#39;</span>],
            <span style="background-color: #fff0f0">&#39;result&#39;</span>: <span style="background-color: #fff0f0">&#39;Ok&#39;</span>,
            <span style="background-color: #fff0f0">&#39;data&#39;</span>: base64<span style="color: #333333">.</span>b64encode(filtered<span style="color: #333333">.</span>encode(<span style="background-color: #fff0f0">&#39;utf-8&#39;</span>) <span style="color: #333333">+</span> b<span style="background-color: #fff0f0">&#39;</span><span style="color: #666666; font-weight: bold; background-color: #fff0f0">\n</span><span style="background-color: #fff0f0">&#39;</span>)<span style="color: #333333">.</span>decode(<span style="background-color: #fff0f0">&#39;utf-8&#39;</span>)
        }
        output<span style="color: #333333">.</span>append(output_record)

    <span style="color: #008800; font-weight: bold">return</span> output
</pre></td></tr></table></div>

The following Kinesis Firehose test event can be used to test the function:

<!-- HTML generated using hilite.me --><div style="background: #ffffff; overflow:auto;width:auto;border:solid gray;border-width:.1em .1em .1em .8em;padding:.2em .6em;"><table><tr><td><pre style="margin: 0; line-height: 125%"> 1
2
3
4
5
6
7
8
9
10
11
12
13
14
15
16
17</pre></td><td><pre style="margin: 0; line-height: 125%">{
<span style="color: #007700">&quot;invocationId&quot;</span>: <span style="background-color: #fff0f0">&quot;invocationIdExample&quot;</span>,
<span style="color: #007700">&quot;deliveryStreamArn&quot;</span>: <span style="background-color: #fff0f0">&quot;arn:aws:kinesis:EXAMPLE&quot;</span>,
<span style="color: #007700">&quot;region&quot;</span>: <span style="background-color: #fff0f0">&quot;us-east-1&quot;</span>,
<span style="color: #007700">&quot;records&quot;</span>: [
{
<span style="color: #007700">&quot;recordId&quot;</span>: <span style="background-color: #fff0f0">&quot;49546986683135544286507457936321625675700192471156785154&quot;</span>,
<span style="color: #007700">&quot;approximateArrivalTimestamp&quot;</span>: <span style="color: #0000DD; font-weight: bold">1495072949453</span>,
<span style="color: #007700">&quot;data&quot;</span>: <span style="background-color: #fff0f0">&quot;R2VvcmdlIFdhc2hpbmd0b24gd2FzIHByZXNpZGVudCBhbmQgaGlzIHNzbiB3YXMgMTIzLTQ1LTY3ODkgYW5kIGhlIGxpdmVkIGF0IDkwMjEwLiBQYXRpZW50IGlkIDAwMDc2YSBhbmQgOTM4MjFhLiBIZSBpcyBvbiBiaW90aW4uIERpYWdub3NlZCB3aXRoIEEwMTAwLg==&quot;</span>
},
{
<span style="color: #007700">&quot;recordId&quot;</span>: <span style="background-color: #fff0f0">&quot;49546986683135544286507457936321625675700192471156785154&quot;</span>,
<span style="color: #007700">&quot;approximateArrivalTimestamp&quot;</span>: <span style="color: #0000DD; font-weight: bold">1495072949453</span>,
<span style="color: #007700">&quot;data&quot;</span>: <span style="background-color: #fff0f0">&quot;R2VvcmdlIFdhc2hpbmd0b24gd2FzIHByZXNpZGVudCBhbmQgaGlzIHNzbiB3YXMgMTIzLTQ1LTY3ODkgYW5kIGhlIGxpdmVkIGF0IDkwMjEwLiBQYXRpZW50IGlkIDAwMDc2YSBhbmQgOTM4MjFhLiBIZSBpcyBvbiBiaW90aW4uIERpYWdub3NlZCB3aXRoIEEwMTAwLg==&quot;</span>
}    
]
}
</pre></td></tr></table></div>

This test event contains 2 messages and the data for each is base 64 encoded, which is the value "He lived in 90210 and his SSN was 123-45-6789." When the test is executed the response will be:

{% raw %}
<!-- HTML generated using hilite.me --><div style="background: #ffffff; overflow:auto;width:auto;border:solid gray;border-width:.1em .1em .1em .8em;padding:.2em .6em;"><table><tr><td><pre style="margin: 0; line-height: 125%">1
2
3
4</pre></td><td><pre style="margin: 0; line-height: 125%">[
<span style="background-color: #fff0f0">&quot;He lived in {{{REDACTED-zip-code}}} and his SSN was {{{REDACTED-ssn}}}.&quot;</span>,
<span style="background-color: #fff0f0">&quot;He lived in {{{REDACTED-zip-code}}} and his SSN was {{{REDACTED-ssn}}}.&quot;</span>
]
</pre></td></tr></table></div>
{% endraw %}

When executing the test, the AWS Lambda function will extract the data from the requests in the firehose and submit each to Philter for filtering. The responses from each request will be returned from the function as a JSON list. Note that in our Python function we are ignoring Philter's self-signed certificate. It is recommended that you use a valid signed [certificate](https://philter.mtnfog.com/how-tos/using-a-signed-ssl-certificate-with-philter) for Philter.

When data is now published to the Kinesis Firehose stream, the data will be processed by the AWS Lambda function and Philter prior to exiting the firehose at its configured destination.

## Processing Data

We can use the AWS CLI to publish data to our Kinesis Firehose stream called **sensitive-text**:

<!-- HTML generated using hilite.me --><div style="background: #ffffff; overflow:auto;width:auto;border:solid gray;border-width:.1em .1em .1em .8em;padding:.2em .6em;"><table><tr><td><pre style="margin: 0; line-height: 125%">1</pre></td><td><pre style="margin: 0; line-height: 125%">aws firehose put-record --delivery-stream-name sensitive-text --record <span style="background-color: #fff0f0">&quot;He lived in 90210 and his SSN was 123-45-6789.&quot;</span>
</pre></td></tr></table></div>

Check the destination S3 bucket and you will have a single object with the following line:

{% raw %}
<!-- HTML generated using hilite.me --><div style="background: #ffffff; overflow:auto;width:auto;border:solid gray;border-width:.1em .1em .1em .8em;padding:.2em .6em;"><table><tr><td><pre style="margin: 0; line-height: 125%">1</pre></td><td><pre style="margin: 0; line-height: 125%">He lived in <span style="color: #333333">{{{</span>REDACTED-zip-code<span style="color: #333333">}}}</span> and his SSN was <span style="color: #333333">{{{</span>REDACTED-ssn<span style="color: #333333">}}}</span>.
</pre></td></tr></table></div>
{% endraw %}

## Conclusion

In this blog post we have created an AWS Firehose pipeline that uses an AWS Lambda function to remove PII and PHI from the text in the streaming pipeline.

## Resources

* [Amazon Kinesis Data Firehose](https://aws.amazon.com/kinesis/data-firehose/)
* [Amazon Kinesis Data Firehose Data Transformation](https://docs.aws.amazon.com/firehose/latest/dev/data-transformation.html)