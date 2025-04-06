document.addEventListener('DOMContentLoaded', function () {
    const questionContainer = document.getElementById('questionContainer');
    const prevBtn = document.getElementById('prevBtn');
    const saveNextBtn = document.getElementById('saveNextBtn');
    const submitTestBtn = document.getElementById('submitTestBtn');
    const fullscreenBtn = document.getElementById('fullscreenBtn');
    const testContent = document.getElementById('test-content');
    const clearOptionBtn = document.getElementById('clearOptionBtn');

    // Sample Questions and Options
    
    var questions = []
    // const test_ques_data =({{test_data}});
    console.log(test_ques_data)
    console.log(typeof test_ques_data)
    console.log(test_ques_data[0].question)
    for(var i=0;i<test_ques_data.length;i++){
        questions.push({
            id : test_ques_data[i].id,
            question : test_ques_data[i].question,
            options : [test_ques_data[i].option_A,test_ques_data[i].option_B,test_ques_data[i].option_C,test_ques_data[i].option_D]
        })
        // (k)
    }
    console.log(questions)

    let currentQuestionIndex = 0;
    let selectedAnswers = new Array(questions.length).fill(null); // Array to store selected answers

    // Initialize the timer
    let timeInSeconds = 0; // 0 seconds initially
    let timerInterval; // Variable to hold the interval for the timer
    const timerElement = document.getElementById('timer');

    // Function to update the timer
    function updateTimer() {
        const minutes = Math.floor(timeInSeconds / 60);
        const seconds = timeInSeconds % 60;
        timerElement.textContent = `${minutes}:${seconds < 10 ? '0' : ''}${seconds}`;

        // Reduce time by 1 second
        timeInSeconds--;

        // Check if time is up
        if (timeInSeconds < 0) {
            clearInterval(timerInterval); // Stop the timer
            submitTest(); // Submit the test
        }
    }

    // Function to initialize the timer
    function initializeTimer() {
        // Set the time (25 minutes)
        timeInSeconds = 25 * 60;
        updateTimer(); // Update timer display initially
        // Call updateTimer every second (1000 milliseconds)
        timerInterval = setInterval(updateTimer, 1000);
    }

    // Function to enable fullscreen mode
    function enableFullscreen() {
        const elem = document.documentElement;
        if (elem.requestFullscreen) {
            elem.requestFullscreen();
        } else if (elem.webkitRequestFullscreen) { /* Safari */
            elem.webkitRequestFullscreen();
        } else if (elem.msRequestFullscreen) { /* IE11 */
            elem.msRequestFullscreen();
        }

        // Start the timer after enabling fullscreen mode
        initializeTimer();
        showTestContent();
    }

    // Function to show the test content
    // Function to show the test content
    function showTestContent() {
        document.querySelector('.test-content').style.display = 'block';
    }


    // Event listener for the fullscreen button
    fullscreenBtn.addEventListener('click', function () {
        enableFullscreen(); // Enable fullscreen mode
        fullscreenBtn.style.display = 'none'; // Hide the fullscreen button
    });

    // Initialize the first question
    displayQuestion();

    // Enable the "Previous" button initially
    prevBtn.disabled = false;

    // Event listener for "Save and Next" button
    saveNextBtn.addEventListener('click', function (event) {
        event.preventDefault();
        // Add logic to save answer and move to the next question
        saveAnswer();
        currentQuestionIndex++;
        if (currentQuestionIndex < questions.length) {
            displayQuestion();
            // Disable "Save & Next" button if it's the last question
            if (currentQuestionIndex === questions.length - 1) {
                saveNextBtn.disabled = true;
            }
        } else {
            // Handle reaching the end of the questions
            // Do nothing when reaching the last question
        }
    });



    // saveNextBtn.addEventListener('click', function () {
    //     saveAnswer();
    //     currentQuestionIndex++;
    //     if (currentQuestionIndex < questions.length) {
    //         displayQuestion();
    //     } else {
    //     }
    // });

    // Event listener for "Submit Test" button
    submitTestBtn.addEventListener('click', function () {
        saveAnswer();
        submitTest(); // Submit the test
    });

    // Event listener for "Previous" button
    // prevBtn.addEventListener('click', function () {
    //     if (currentQuestionIndex > 0) {
    //         currentQuestionIndex--;
    //         displayQuestion();
    //     }
    // });

    // Event listener for "Previous" button
    prevBtn.addEventListener('click', function (event) {
        event.preventDefault();
        // Move to the previous question if available
        if (currentQuestionIndex > 0) {
            currentQuestionIndex--;
            displayQuestion();
            
            // Enable "Save & Next" button if it's not the last question
            if (currentQuestionIndex < questions.length - 1) {
                saveNextBtn.disabled = false;
            }
        }
    });


    // Function to display the current question
    function displayQuestion() {
        const currentQuestion = questions[currentQuestionIndex];
        const optionsHTML = currentQuestion.options.map((option, index) => {
            return `<label for="option${index + 1}">
                        <input type="radio" name="options" id="option${index + 1}" value="${index + 1}" ${selectedAnswers[currentQuestionIndex] === index ? 'checked' : ''}>
                        ${option}
                    </label>`;
        }).join('');

        questionContainer.innerHTML = `
            <div class="question">
                <p>${currentQuestionIndex+1}.${currentQuestion.question}</p>
                <div class="options-container">${optionsHTML}</div>
            </div>
        `;

        // Disable "Previous" button if at the first question
        prevBtn.disabled = currentQuestionIndex === 0;
    }

    // Function to save the selected answer
    function saveAnswer() {
        const selectedOption = document.querySelector('input[name="options"]:checked');
        if (selectedOption) {
            const answerIndex = parseInt(selectedOption.value) - 1;
            selectedAnswers[currentQuestionIndex] = answerIndex;
            // Add logic to save the selected answer (if needed)
            console.log(`Question ${currentQuestionIndex + 1} Answer: ${questions[currentQuestionIndex].options[answerIndex]}`);
        }
    }

    clearOptionBtn.addEventListener('click', function (event) {
        event.preventDefault();
        clearSelectedOption();
    });

    function clearSelectedOption() {
        const selectedOption = document.querySelector('input[name="options"]:checked');
        if (selectedOption) {
            selectedOption.checked = false;
            selectedAnswers[currentQuestionIndex] = null;
        }
    }
    
    // Function to submit the test
    function submitTest() {
        // Redirect to the report page
        window.location.href = "/TestAnalytics?testCompleted=true";
        console.log(selectedAnswers)
        var answers = []
        for(var i=0;i<questions.length;i++){
            answers.push({
                id:questions[i].id,
                answer:selectedAnswers[i]
            })
            console.log(answers[i])
        }
        console.log(answers)
        submitTestBtn.value = JSON.stringify(answers);
        document.getElementById("testForm").submit()
    }
});
