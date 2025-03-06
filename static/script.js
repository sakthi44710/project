function visualizeCareer(careerPathJson) {
    try {
        const careerPath = JSON.parse(careerPathJson);
        const viz = document.getElementById('visualization');
        if (!viz) {
            console.error("Visualization element not found");
            return;
        }
        viz.innerHTML = `
            <h3>Career Path Steps</h3>
            <ul>
                ${careerPath.map((step, index) => `<li><strong>Step ${index + 1}:</strong> ${step}</li>`).join('')}
            </ul>
        `;
        viz.style.opacity = 0;
        setTimeout(() => {
            viz.style.transition = 'opacity 0.5s';
            viz.style.opacity = 1;
        }, 100);
    } catch (e) {
        console.error("Error parsing career path:", e);
        document.getElementById('visualization').innerHTML = "<p>Error loading career path. Please try again.</p>";
    }
}