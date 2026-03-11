# Configuração de remoto local para desenvolvimento

Este repositório foi configurado com um remoto `origin` apontando para um bare repo local em `/tmp/bot_unb_origin.git`.

Passos executados:

1. Validação de remoto com `git remote -v`.
2. Criação de remoto local com `git init --bare /tmp/bot_unb_origin.git`.
3. Associação de `origin` com `git remote add origin /tmp/bot_unb_origin.git`.
4. Publicação e tracking do branch `work` com `git push -u origin work`.
5. Sincronização com `git pull`.
