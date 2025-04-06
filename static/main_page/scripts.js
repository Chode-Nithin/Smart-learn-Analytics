// document.addEventListener('DOMContentLoaded', function () {
//     // Get elements
//     const signupForm = document.getElementById('signupForm');
//     const passwordInput = document.getElementById('signupPassword');
//     const togglePassword = document.getElementById('togglePassword');
//     const passwordError = document.getElementById('passwordError');

//     // Object to store registered users' information
//     const registeredUsers = {};

//     // Event listener for signup form submission
//     signupForm.addEventListener('submit', function (e) {
//         e.preventDefault();

//         const email = document.getElementById('signupEmail').value;
//         const password = passwordInput.value;

//         // Password validation
//         const lengthRegex = /^.{8,15}$/;
//         const uppercaseRegex = /[A-Z]/;
//         const lowercaseRegex = /[a-z]/;
//         const specialCharacterRegex = /[-!@#$%^&*()_+|~=`{}\[\]:";'<>?,.\/]/;
//         const numericalRegex = /[0-9]/;

//         const isValidLength = lengthRegex.test(password);
//         const hasUppercase = uppercaseRegex.test(password);
//         const hasLowercase = lowercaseRegex.test(password);
//         const hasSpecialCharacter = specialCharacterRegex.test(password);
//         const hasNumerical = numericalRegex.test(password);

//         if (!isValidLength) {
//             passwordError.textContent = 'Password length should be between 8 and 15 characters';
//             return; // Prevent form submission if validation fails
//         } else if (!hasUppercase) {
//             passwordError.textContent = 'Password should contain at least one uppercase letter';
//             return;
//         } else if (!hasLowercase) {
//             passwordError.textContent = 'Password should contain at least one lowercase letter';
//             return;
//         } else if (!hasSpecialCharacter) {
//             passwordError.textContent = 'Password should contain at least one special character';
//             return;
//         } else if (!hasNumerical) {
//             passwordError.textContent = 'Password should contain at least one numerical digit';
//             return;
//         } else {
//             passwordError.textContent = '';
//         }

//         document.getElementById('signupForm').submit();
//         // Store user information
//         // registeredUsers[email] = password;
//         // alert('Registration successful! You can now login.');
//         // window.location.href = '/signup';
//     });

//     // Event listener for password input validation
//     passwordInput.addEventListener('input', function () {
//         const password = passwordInput.value;

//         // Password validation logic (same as above)
//         // You can refactor the password validation code here if you want
//     });

//     // // Event listener for toggling password visibility
//     // togglePassword.addEventListener('click', function () {
//     //     const type = passwordInput.getAttribute('type') === 'password' ? 'text' : 'password';
//     //     passwordInput.setAttribute('type', type);

//     //     // Change eye icon based on password visibility
//     //     togglePassword.querySelector('i').classList.toggle('fa-eye');
//     //     togglePassword.querySelector('i').classList.toggle('fa-eye-slash');
//     // });
// });



// document.addEventListener('DOMContentLoaded', function () {
//     // Function to handle form submission
//     function submitForm(event) {
//         event.preventDefault(); // Prevent default form submission

//         // Get form elements
//         const signupForm = document.getElementById('signupForm');
//         const passwordInput = document.getElementById('signupPassword');
//         const passwordError = document.getElementById('passwordError');

//         // Your validation and form submission logic here
//         // This part is the same as in your original submitForm() function
        
//         // Example validation (replace with your own validation logic)
//         const password = passwordInput.value;
//         if (password.length < 8) {
//             passwordError.textContent = 'Password should be at least 8 characters long';
//             return;
//         }

//         // If validation passes, submit the form
//         signupForm.submit();
//     }

//     // Add event listener to form submission
//     const signupForm = document.getElementById('signform');
//     signupForm.addEventListener('submit', submitForm);
// });




// function submitForm() {
    
//     const signupForm = document.getElementById('signupForm');
//     const passwordInput = document.getElementById('signupPassword');
//     const togglePassword = document.getElementById('togglePassword');
//     const passwordError = document.getElementById('passwordError');
//     console.log(signupForm)


//     const email = document.getElementById('signupEmail').value;
//     const password = passwordInput.value;

//     // Password validation
//     const lengthRegex = /^.{8,15}$/;
//     const uppercaseRegex = /[A-Z]/;
//     const lowercaseRegex = /[a-z]/;
//     const specialCharacterRegex = /[-!@#$%^&*()_+|~=`{}\[\]:";'<>?,.\/]/;
//     const numericalRegex = /[0-9]/;

//     const isValidLength = lengthRegex.test(password);
//     const hasUppercase = uppercaseRegex.test(password);
//     const hasLowercase = lowercaseRegex.test(password);
//     const hasSpecialCharacter = specialCharacterRegex.test(password);
//     const hasNumerical = numericalRegex.test(password);
//     if (!isValidLength) {
//         passwordError.textContent = 'Password length should be between 8 and 15 characters';
//         return; // Prevent form submission if validation fails
//     } else if (!hasUppercase) {
//         passwordError.textContent = 'Password should contain at least one uppercase letter';
//         return;
//     } else if (!hasLowercase) {
//         passwordError.textContent = 'Password should contain at least one lowercase letter';
//         return;
//     } else if (!hasSpecialCharacter) {
//         passwordError.textContent = 'Password should contain at least one special character';
//         return;
//     } else if (!hasNumerical) {
//         passwordError.textContent = 'Password should contain at least one numerical digit';
//         return;
//     } else {
//         passwordError.textContent = '';
//     }
//     document.getElementById('signupForm').submit();
// }




document.addEventListener('DOMContentLoaded', function () {
    // Function to handle form submission
    function submitForm() {
        // Get form elements
        // const passwordInput = document.getElementById('signupPassword');
        // const confirmPasswordInput = document.getElementById('confirmPassword');
        // const passwordError = document.getElementById('passwordError');

        // Example password validation
        // const password = passwordInput.value;
        // if (password.length < 8) {
        //     passwordError.textContent = 'Password should be at characters long';
        //     return false; // Prevent form submission
        // }

        // const confirmPassword = confirmPasswordInput.value;
        // if (password !== confirmPassword) {
        //     passwordError.textContent = 'Passwords do not match';
        //     return false; // Prevent form submission
        // }

        // If validation passes, return true to allow form submission
        // passwordError.textContent = ''; // Clear any previous error messages
        return true;
    }

    
    const passwordInput = document.getElementById('signupPassword');
    const Conpassword = document.getElementById('confirmPassword');
    const phoneNumber = document.getElementById('signupPhoneNumber');
    const emailId = document.getElementById('signupEmail');

    // Update password error message when password input changes
    passwordInput.addEventListener('input', function () {
        const passwordError = document.getElementById('passwordError');
        const password = passwordInput.value;

        // Password validation
        const lengthRegex = /^.{8,15}$/;
        const uppercaseRegex = /[A-Z]/;
        const lowercaseRegex = /[a-z]/;
        const specialCharacterRegex = /[-!@#$%^&*()_+|~=`{}\[\]:";'<>?,.\/]/;
        const numericalRegex = /[0-9]/;

        const isValidLength = lengthRegex.test(password);
        const hasUppercase = uppercaseRegex.test(password);
        const hasLowercase = lowercaseRegex.test(password);
        const hasSpecialCharacter = specialCharacterRegex.test(password);
        const hasNumerical = numericalRegex.test(password);
        if (!isValidLength) {
            passwordError.textContent = 'Password length should be between 8 and 15 characters';
            return; // Prevent form submission if validation fails
        } else if (!hasUppercase) {
            passwordError.textContent = 'Password should contain at least one uppercase letter';
            return;
        } else if (!hasLowercase) {
            passwordError.textContent = 'Password should contain at least one lowercase letter';
            return;
        } else if (!hasSpecialCharacter) {
            passwordError.textContent = 'Password should contain at least one special character';
            return;
        } else if (!hasNumerical) {
            passwordError.textContent = 'Password should contain at least one numerical digit';
            return;
        } else if (Conpassword.value !='' && Conpassword.value != password){
            passwordError.textContent = 'Passwords should be equal';
        }
        else {
            passwordError.textContent = '';
        }
    });

    
    // Update password error message when confirm password input changes
    Conpassword.addEventListener('input', function () {
        const passwordError = document.getElementById('passwordError');
        if (this.value === passwordInput.value ) {
            passwordError.textContent = '';
        } else {
            passwordError.textContent = 'Passwords should be equal';
        }
    });

    // Update password error message when phone number input changes
    phoneNumber.addEventListener('input', function () {
        const phone = phoneNumber.value
        const passwordError = document.getElementById('passwordError');
        const phoneRegex = /^\d{10}$/; // Regex to match exactly 10 digits
        if (!phoneRegex.test(phone)) {
            passwordError.textContent = 'Phone number must be 10 digits';
        } else {
            passwordError.textContent = ' ';
        }
    });


    // Update password error message when email id input changes
    emailId.addEventListener('input', function () {
        const email = emailId.value
        const passwordError = document.getElementById('passwordError');
        const emailRegex = /^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/; // Regex for email
        if (!emailRegex.test(email)) {
            passwordError.textContent = 'Enter a valid email address';
        } else {
            passwordError.textContent = ' ';
        }
    });

});
