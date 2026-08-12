document.getElementById('downloadForm').addEventListener('submit', async (e) => {
    e.preventDefault();

    const mediaUrl = document.getElementById('mediaUrl').value;
    const statusContainer = document.getElementById('statusContainer');
    const statusMessage = document.getElementById('statusMessage');
    const loader = document.getElementById('loader');
    const downloadLink = document.getElementById('downloadLink');
    const submitBtn = document.getElementById('submitBtn');

    statusContainer.classList.remove('hidden');
    loader.classList.remove('hidden');
    downloadLink.classList.add('hidden');
    submitBtn.disabled = true;
    statusMessage.textContent = 'Обработка... (Analisando link e preparando download...)';

    try {
        const response = await fetch('/api/download', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ url: mediaUrl })
        });

        const data = await response.json();

        loader.classList.add('hidden');
        submitBtn.disabled = false;

        if (data.success) {
            statusMessage.textContent = data.message;
            downloadLink.href = data.fileUrl;
            downloadLink.classList.remove('hidden');
        } else {
            statusMessage.textContent = `❌ Erro: ${data.message}`;
        }
    } catch (err) {
        loader.classList.add('hidden');
        submitBtn.disabled = false;
        statusMessage.textContent = '❌ Falha ao se conectar com o servidor da Alya Bot.';
    }
});
