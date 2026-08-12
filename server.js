const express = require('express');
const { spawn } = require('child_process');
const path = require('path');
const fs = require('fs');

const app = express();
const PORT = process.env.PORT || 3000;

app.use(express.json());
app.use(express.static(path.join(__dirname, 'public')));

// Servidor estático para a pasta de mídias categorizada
const mediaDir = path.join(__dirname, 'media');
app.use('/media', express.static(mediaDir));

if (!fs.existsSync(mediaDir)) {
    fs.mkdirSync(mediaDir, { recursive: true });
}

app.post('/api/download', (req, res) => {
    const { url } = req.body;

    if (!url) {
        return res.status(400).json({ success: false, message: 'Insira uma URL válida!' });
    }

    console.log(`[+] Baixando mídia da URL: ${url}`);

    const pythonProcess = spawn('python', ['download.py', url]);

    let dataString = '';
    let errorString = '';

    pythonProcess.stdout.on('data', (data) => {
        dataString += data.toString();
    });

    pythonProcess.stderr.on('data', (data) => {
        errorString += data.toString();
    });

    pythonProcess.on('close', (code) => {
        if (errorString) {
            console.error(`[Python Stderr]: ${errorString}`);
        }

        try {
            const match = dataString.match(/JSON_RESULT:(.+)/);
            if (!match) {
                throw new Error('Não foi possível processar a resposta do script.');
            }

            const result = JSON.parse(match[1].trim());

            if (result.status === 'success') {
                console.log(`[✓] Salvo em: media/${result.relative_path}`);
                return res.json({
                    success: true,
                    message: `Мило! Mídia do ${result.platform.toUpperCase()} baixada com sucesso!`,
                    fileUrl: `/media/${result.relative_path}`,
                    filename: result.filename,
                    platform: result.platform,
                    mediaType: result.media_type
                });
            } else {
                console.error(`[×] Erro no Python: ${result.message}`);
                return res.status(400).json({ success: false, message: result.message });
            }
        } catch (e) {
            console.error(`[×] Erro no parse: ${e.message}`);
            return res.status(500).json({
                success: false,
                message: 'Erro ao processar o download.',
                details: e.message
            });
        }
    });
});

app.listen(PORT, () => {
    console.log(`❄️ Alya Media Downloader rodando na porta ${PORT}`);
});
