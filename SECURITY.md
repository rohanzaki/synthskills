# Security policy

SynthSkills is a public beta. If you find a security problem in the service, in
the access-key flow, or in anything in this repository, please report it
privately.

**Email:** contact@rohanzakie.com

Please include what you found, how to reproduce it, and which client you used.
Do not open a public issue for a vulnerability.

## Never post keys

Access keys (`ssk_...`), passes and claim codes are secrets.

- Never paste them into an issue, a pull request, a discussion, a log or a screenshot.
- If you posted one by mistake, rotate it at once: call `rotate_key(access_key=<your key>)`,
  save the new key, and accept the charter again. If you cannot, write to the address above
  with the key's `key_hint` (the last four characters), never the key itself.

## Scope

In scope: the public service at https://synthskills.synthminds.pk, and the files in this repository.
Out of scope: denial-of-service testing, crawling or bulk reading of the library (it is
against the charter and suspends keys), and social engineering.

I will acknowledge a report as soon as I can. This is a one-person beta, so please be patient.
