// let n = 10

// let sum = 0
// for (let i = 1; i <= 10; i++) {
//     sum += i
// }
// console.log(sum)
// 1부터 n까지 합 구하는 함수
function Sum1to10(num) {
    let sum = 0
    for (let i = 1; i <= num; i++) {
        sum += i
    }
    return sum
}

console.log(Sum1to10(100))
