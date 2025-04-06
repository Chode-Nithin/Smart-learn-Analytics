document.addEventListener('DOMContentLoaded', function () {
    const agreeCheckbox = document.getElementById('agreeCheckbox');
    const startTestBtn = document.getElementById('startTestBtn');

    agreeCheckbox.addEventListener('change', function () {
        startTestBtn.disabled = !agreeCheckbox.checked;
    });
});
function startTest(option) {
    // Assuming you want to redirect to test.html
    console.log("dgg",option)
    document.getElementById('instOption').value = option;
    document.getElementById('instForm').submit();
    window.location.href = '/Test';
    
}
