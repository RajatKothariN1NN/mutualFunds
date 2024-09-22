const aiModal = document.getElementById('ai-modal');
const aiButton = document.getElementById('ai-recommendation-btn');
const closeButton = document.querySelector('.close');
const nextStepButton = document.getElementById('next-step');
const prevStepButton = document.getElementById('prev-step');

let currentStep = 0;
const steps = [
    "Select your Fund Type.",
    "Choose your Risk Profile.",
    "Select Themes you are interested in.",
    "Define your Investment Duration.",
    "Estimate your Expected Returns."
];

aiButton.onclick = function() {
    aiModal.style.display = "block";
    showStep(currentStep);
};

closeButton.onclick = function() {
    aiModal.style.display = "none";
};

nextStepButton.onclick = function() {
    if (currentStep < steps.length - 1) {
        currentStep++;
        showStep(currentStep);
    }
};

prevStepButton.onclick = function() {
    if (currentStep > 0) {
        currentStep--;
        showStep(currentStep);
    }
};

function showStep(stepIndex) {
    document.getElementById('recommendation-steps').innerText = steps[stepIndex];
    prevStepButton.style.display = stepIndex === 0 ? "none" : "inline";
    nextStepButton.style.display = stepIndex === steps.length - 1 ? "none" : "inline";
}

window.onclick = function(event) {
    if (event.target === aiModal) {
        aiModal.style.display = "none";
    }
};
