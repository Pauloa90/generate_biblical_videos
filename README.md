# 🎬 Biblical Videos Generator

Gerador automático de vídeos bíblicos usando a API Kling da Piapi. Cria 5 cenas da história de David e Golias com personagens consistentes e animação estilo Pixar.

## 📋 Características

- **5 cenas bíblicas** com narrativa completa
- **Personagens consistentes** (David, Saul, Golias)
- **Backgrounds únicos** para cada cena
- **Animação estilo Pixar 3D**
- **Movimentação de câmera** cinematográfica
- **Vídeos de 5 segundos** em 1080p (16:9)
- **Geração paralela** para maior velocidade
- **Retry automático** em caso de falha

## 🚀 Configuração Rápida

### 1. Fork este repositório

Clique no botão "Fork" no topo da página.

### 2. Obtenha sua API Key da Piapi

1. Acesse [https://app.piapi.ai/](https://app.piapi.ai/)
2. Crie uma conta ou faça login
3. Vá para Settings > API Keys
4. Copie sua API key

### 3. Configure os Secrets do GitHub

No seu repositório fork:
1. Vá para Settings > Secrets and variables > Actions
2. Clique em "New repository secret"
3. Adicione:
   - **Name**: `PIAPI_API_KEY`
   - **Value**: Sua API key da Piapi

### 4. Adicione as imagens

#### Opção A: Usando o GitHub (Recomendado)

1. Crie uma pasta `images/` no seu repositório
2. Faça upload das imagens:
   - `David.png` - Imagem do personagem David
   - `Saul.png` - Imagem do personagem Saul
   - `Golias.png` - Imagem do personagem Golias
   - `bg1.png` - Background para cena 1 (David com ovelhas)
   - `bg2.png` - Background para cena 2 (Tenda do rei Saul)
   - `bg3.png` - Background para cena 3 (Caminho para o acampamento)
   - `bg4.png` - Background para cena 4 (Colina onde Golias desafia)
   - `bg5.png` - Background para cena 5 (Acampamento com soldados)

3. Atualize o arquivo `generate_biblical_videos.py`:
   ```python
   GITHUB_IMAGES_BASE = "https://raw.githubusercontent.com/SEU_USUARIO/SEU_REPO/main/images/"
   ```

#### Opção B: Usando Google Drive

1. Faça upload das imagens para o Google Drive
2. Para cada imagem, clique com botão direito > "Obter link"
3. Certifique-se que o link está como "Qualquer pessoa com o link pode ver"
4. Extraia o FILE_ID do link (parte entre `/d/` e `/view`)
5. Atualize o arquivo `generate_biblical_videos.py` com os IDs

### 5. Execute o Workflow

1. Vá para a aba "Actions" do seu repositório
2. Selecione "Generate Biblical Videos"
3. Clique em "Run workflow"
4. Escolha as opções:
   - **Which scenes to generate**: `all` (todas as cenas)
   - **Generate videos in parallel**: `true` (mais rápido)
5. Clique em "Run workflow" (botão verde)

## 📊 Monitoramento

Durante a execução:
- Acompanhe o progresso em tempo real na aba Actions
- Cada cena leva aproximadamente 1-3 minutos
- O processo total leva cerca de 5-15 minutos

Após a conclusão:
- Veja o resumo com links dos vídeos no Summary
- Baixe o arquivo JSON com todos os resultados em Artifacts

## 💰 Custos

- Cada vídeo de 5 segundos em modo Professional: $0.96
- Custo total para 5 cenas: ~$4.80
- Certifique-se de ter créditos suficientes na sua conta Piapi

## 🎬 Descrição das Cenas

### Cena 1: David com as ovelhas
David jovem pastor cuidando pacificamente de suas ovelhas no campo.

### Cena 2: Saul preocupado
Rei Saul sentado em seu trono, mostrando preocupação e incerteza.

### Cena 3: David chega ao acampamento
David correndo determinado em direção ao acampamento militar.

### Cena 4: Golias desafia o exército
O gigante Golias no topo da colina, desafiando o exército de Israel.

### Cena 5: David se voluntaria
David se apresenta corajosamente entre os soldados surpresos.

## 🔧 Personalização

### Modificar prompts das cenas
Edite o array `SCENES` em `generate_biblical_videos.py`

### Ajustar movimentos de câmera
Modifique os valores em `camera_movement` para cada cena:
- `horizontal`: Movimento lateral (-20 a 20)
- `vertical`: Movimento vertical (-20 a 20)
- `pan`: Rotação horizontal
- `tilt`: Rotação vertical
- `zoom`: Aproximação/afastamento

### Mudar duração ou qualidade
- Duração: Mude `"duration": 5` (5 ou 10 segundos)
- Modo: Mude `"mode": "pro"` para `"std"` (mais barato)
- Aspect ratio: Mude `"aspect_ratio": "16:9"` (opções: 1:1, 9:16, 16:9)

## 🆘 Solução de Problemas

### "API key not found"
- Verifique se adicionou o secret `PIAPI_API_KEY` corretamente

### "Failed to create task"
- Verifique se tem créditos na conta Piapi
- Confirme se as URLs das imagens estão acessíveis

### "Task timeout"
- Normal para vídeos complexos, o sistema fará retry automático

### Imagens não carregam
- Se usar GitHub: Certifique-se que fez commit das imagens
- Se usar Google Drive: Verifique se os links são públicos

## 📝 Output

O sistema gera:
1. **Arquivos de vídeo**: URLs diretas para download/visualização
2. **Arquivo JSON**: Resumo completo com todos os detalhes
3. **GitHub Summary**: Resumo visual no Actions

Exemplo de output JSON:
```json
{
  "generation_date": "2024-03-10T10:30:00",
  "total_scenes": 5,
  "successful": 5,
  "failed": 0,
  "total_time_seconds": 420,
  "results": [
    {
      "scene_id": 1,
      "scene_name": "David with the sheep",
      "status": "completed",
      "video_url": "https://...",
      "task_id": "..."
    }
  ]
}
```

## 🚀 Próximos Passos

1. **Download dos vídeos**: Use as URLs geradas para baixar os vídeos
2. **Edição**: Junte os 5 vídeos em um editor para criar o filme completo
3. **Upload para YouTube**: Configure aspect ratio 16:9, 1080p

## 📞 Suporte

- **Documentação Piapi**: https://piapi.ai/docs/kling-api
- **Discord Piapi**: Para suporte técnico
- **Issues**: Abra uma issue neste repositório
