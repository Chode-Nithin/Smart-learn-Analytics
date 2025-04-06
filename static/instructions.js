document.addEventListener('DOMContentLoaded', function () {
    const agreeCheckbox = document.getElementById('agreeCheckbox');
    const startTestBtn = document.getElementById('startTestBtn');

    agreeCheckbox.addEventListener('change', function () {
        startTestBtn.disabled = !agreeCheckbox.checked;
    });

    startTestBtn.addEventListener('mouseover', function () {
        if (!agreeCheckbox.checked) {
            alert("Please acknowledge the instructions by checking the checkbox before starting the test.");
        }
    });
});

function startTest(option) {
    // Assuming you want to redirect to test.html
    console.log("dgg",option)
    document.getElementById('instOption').value = option;
    document.getElementById('instForm').submit();
    window.location.href = 'test.html';
}