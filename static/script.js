function visualizeCareer() {
    const viz = document.getElementById('visualization');
    viz.innerHTML = `
        <h3>Career Path Visualization</h3>
        <p><strong>Step 1:</strong> Learn foundational skills</p>
        <p><strong>Step 2:</strong> Gain experience (internships/projects)</p>
        <p><strong>Step 3:</strong> Apply for entry-level roles</p>
        <p><strong>Step 4:</strong> Advance to senior positions</p>
    `;
    viz.style.opacity = 0;
    setTimeout(() => {
        viz.style.transition = 'opacity 0.5s';
        viz.style.opacity = 1;
    }, 100);
}