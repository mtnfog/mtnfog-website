#! /usr/bin/perl

# See https://docs.aws.amazon.com/ses/latest/dg/send-email-sendmail.html for using sendmail with AWS SES.

use strict;
use CGI;
my $mailer = '/usr/sbin/sendmail -t';

# ---- Read values from the form ----
my $query = new CGI;
my $thanks_url = 'https://www.mtnfog.com/thanks';
#my $thanks_url = $query->param('thanks');
#my $sendto = $query->param('sendto');
#my $sendto = 'jeff.zemerick\@mtnfog.com';
my $name = $query->param('name');
my $email = $query->param('email');
#my $subject = $query->param('subject');
#my $message = $query->param('message');
#my $from = $name." <".$email.">";

use Email::Simple;
use Email::Simple::Creator;
use Email::Sender::Simple qw(sendmail);

my $email = Email::Simple->create(
 header => [
       From => "jeff.zemerick\@mtnfog.com",
       To => "jeff.zemerick\@mtnfog.com",
       Subject => "Consultation Request",
 ],
 body => "This is a request for a document redaction consultation:\n\nName: $name\nEmail: $email"
);
sendmail($email);

# ---- Show Confirmation ----
print "Content-type: text/html\n\n";
print "<html><head>";
print "<META HTTP-EQUIV=\"refresh\" CONTENT=\"1; URL=".$thanks_url."\">";
print "</head></html>";

