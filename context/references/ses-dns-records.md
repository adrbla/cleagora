# AWS SES DNS Records for cleagora.com

Region: eu-west-3 (Paris)

## Domain verification (TXT)

- Type: TXT
- Name: `_amazonses.cleagora.com`
- Value: `GLEzTmf5+t/QDgWmWI5fTYLUpWl+lspUnLUFX5LjtVM=`

## DKIM (3 CNAME records)

- Type: CNAME
- Name: `ihz7wilhymnvliatizsnkgjmr7tluqqe._domainkey.cleagora.com`
- Value: `ihz7wilhymnvliatizsnkgjmr7tluqqe.dkim.amazonses.com`

- Type: CNAME
- Name: `uwtygezzudhb2jqw45ikqzt7gwdqyspf._domainkey.cleagora.com`
- Value: `uwtygezzudhb2jqw45ikqzt7gwdqyspf.dkim.amazonses.com`

- Type: CNAME
- Name: `ro4sg7agjciumq3rrtdn356wefb3xnde._domainkey.cleagora.com`
- Value: `ro4sg7agjciumq3rrtdn356wefb3xnde.dkim.amazonses.com`

## SPF (TXT)

- Type: TXT
- Name: `cleagora.com`
- Value: `v=spf1 include:amazonses.com ~all`

## DMARC (TXT)

- Type: TXT
- Name: `_dmarc.cleagora.com`
- Value: `v=DMARC1; p=none; rua=mailto:ab@ubyx.com`
