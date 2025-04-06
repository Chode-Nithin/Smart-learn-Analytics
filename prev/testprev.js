document.addEventListener('DOMContentLoaded', function () {
    const container = document.getElementById('container');
    const main = document.getElementById('main');
    const questionContainer = document.getElementById('questionContainer');
    const prevBtn = document.getElementById('prevBtn');
    const saveNextBtn = document.getElementById('saveNextBtn');
    const submitTestBtn = document.getElementById('submitTestBtn');
    const options = document.querySelectorAll('input[name="options"]');
    const NUM_OPTIONS = 4; // Number of options for each question

    const fullscreenBtn = document.getElementById('fullscreenBtn');
    const testContent = document.querySelector('.test-content');
    const startTestBtn = document.getElementById('startTestBtn');




    fullscreenBtn.addEventListener('click', function () {
                enableFullscreen(); // Enable fullscreen mode
                showTestContent(); // Show the test content
                startTestBtn.disabled = false; // Enable the start button
            });
        
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
            }
        
            // Function to show the test content
            function showTestContent() {
                testContent.style.display = 'block';
            }
        
            // Function to handle test completion and redirection
            function completeTestAndRedirect() {
                // Add your logic for completing the test here
                // Redirect to analytics page after test completion
                window.location.href = "/TestAnalytics?testCompleted=true";
            }

             
            //  var selectedAnswers = []
            // Prevent default form submission behavior
            // form.addEventListener("submit", function(event) {
            //     event.preventDefault();
            // });
        
            // Event listener for the submit test button
            // const submitTestBtn = document.getElementById('submitTestBtn');
            submitTestBtn.addEventListener('click', function () {
                completeTestAndRedirect();
                submitTest()
                
            });



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

    // var questions = [
    //     {
    //         question: "What is the full form of ML?",
    //         options: [
    //             "Machine Learning",
    //             "Math Learning",
    //             "Machine Lifting",
    //             "None of the above"
    //         ]
    //     },
    //     {
    //         question: "Which of the following options identifies the one which is not a type of learning?",
    //         options: [
    //             "Semi Unsupervised Learning",
    //             "Supervised Learning",
    //             "Reinforcement Learning",
    //             "Unsupervised Learning"
    //         ]
    //     }
    //     // Add more questions as needed
    // ];
    // console.log(typeof questions)
    let currentQuestionIndex = 0;
    selectedAnswers = new Array(questions.length).fill(null); // Array to store selected answers

    // Initialize the timer
    let timeInSeconds = 25 * 60; // 25 minutes
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


    // Call updateTimer every second (1000 milliseconds)
    const timerInterval = setInterval(updateTimer, 1000);

    // Initialize the first question
    displayQuestion();

    // Enable the "Previous" button initially
    prevBtn.disabled = false;


   










    // Event listener for "Save and Next" button
    saveNextBtn.addEventListener('click', function (event) {
        // Add logic to save answer and move to the next question
        event.preventDefault();
        saveAnswer();
        currentQuestionIndex++;
        if (currentQuestionIndex < questions.length) {
            displayQuestion();
        } else {
            // Handle reaching the end of the questions
            // Do nothing when reaching the last question
        }
    });

    // Event listener for "Submit Test" button
    // submitTestBtn.addEventListener('click', function (event) {
    //     event.preventDefault();
    //     submitTest();
    //      // Submit the test
    // });

    // Event listener for "Previous" button
    prevBtn.addEventListener('click', function (event) {
        event.preventDefault();
        // Move to the previous question if available
        if (currentQuestionIndex > 0) {
            currentQuestionIndex--;
            displayQuestion();
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
            <p>${currentQuestionIndex+1}.${currentQuestion.question}</p>
            <div class="options-container">${optionsHTML}</div>
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
            console.log(questions[currentQuestionIndex])
        }
    }

    // Function to submit the test
    function submitTest() {
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
