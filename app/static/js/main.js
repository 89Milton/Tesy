document.addEventListener('DOMContentLoaded', () => {
    const spotifyConnectBtn = document.getElementById('spotify-connect');
    const bookSearchInput = document.getElementById('book-search');
    const searchBtn = document.getElementById('search-btn');
    const resultsSection = document.getElementById('results');

    // Update Spotify button based on authentication status
    if (window.isAuthenticated) {
        spotifyConnectBtn.textContent = 'Analyze My Music Taste';
        spotifyConnectBtn.classList.add('authenticated');
    }

    // Spotify Connect/Analyze Button
    spotifyConnectBtn.addEventListener('click', async () => {
        if (!window.isAuthenticated) {
            // Redirect to Spotify login
            window.location.href = '/spotify/login';
            return;
        }

        try {
            // Get user's music taste
            const response = await fetch('/spotify/get-user-taste');
            const data = await response.json();

            if (response.ok) {
                displayMusicAnalysis(data);
            } else {
                console.error('Error:', data.error);
            }
        } catch (error) {
            console.error('Error analyzing music taste:', error);
        }
    });

    // Book Search
    searchBtn.addEventListener('click', async () => {
        const query = bookSearchInput.value.trim();
        if (!query) return;

        try {
            // TODO: Implement book search API call
            console.log('Searching for:', query);
        } catch (error) {
            console.error('Error searching for books:', error);
        }
    });

    // Enter key for book search
    bookSearchInput.addEventListener('keypress', (e) => {
        if (e.key === 'Enter') {
            searchBtn.click();
        }
    });

    function displayMusicAnalysis(data) {
        const { tracks, features } = data;
        
        // Create HTML for displaying tracks and features
        const tracksHtml = tracks.map(track => `
            <div class="track-item">
                <img src="${track.album.images[2].url}" alt="${track.name}" class="track-image">
                <div class="track-info">
                    <h3>${track.name}</h3>
                    <p>${track.artists[0].name}</p>
                </div>
            </div>
        `).join('');

        const featuresHtml = Object.entries(features).map(([key, value]) => `
            <div class="feature-item">
                <span class="feature-label">${key}</span>
                <div class="feature-bar">
                    <div class="feature-value" style="width: ${value * 100}%"></div>
                </div>
            </div>
        `).join('');

        resultsSection.innerHTML = `
            <div class="analysis-container">
                <h2>Your Music Analysis</h2>
                <div class="tracks-container">
                    ${tracksHtml}
                </div>
                <div class="features-container">
                    ${featuresHtml}
                </div>
            </div>
        `;
    }
}); 