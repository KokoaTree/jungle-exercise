// let x = 23

// if (x >= 20) {
//     console.log("성인입니다.")
// } else if (x > 13) {
//     console.log("청소년입니다.")
// } else {
//     console.log("어린이입니다.")
// }

// x = 10

// if (x >= 20) {
//     console.log("성인입니다.")
// } else if (x > 13) {
//     console.log("청소년입니다")
// } else {
//     console.log("어린이입니다.")
// }

// function is_adult(age) {
//     if (age >= 20) {
//         console.log("성인입니다.")
//     } else if (age > 13) {
//         console.log("청소년입니다.")
//     } else {
//         console.log("어린이입니다.")
//     }
// }

// is_adult(29)
// let age1 = 17
// is_adult(age1)
// let age2 = 5
// is_adult(age2)\

function I_am_a(age, gender) {
    if (age < 20 && gender=="남") {
        console.log("I am a boy.")
    } else if (gender == "남") {
        console.log("I am a man.") 
    } else if (age < 20 && gender == "여") {
        console.log("I am a girl.")
    } else if (gender == "여") {
        console.log("I am a woman")
    } else {
        console.log("I am who I am")
    }
}

I_am_a(30, "남")
I_am_a(55, "여")
I_am_a(5, "남")
I_am_a(17, "여")