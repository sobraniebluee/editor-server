function
require
()
{
    return
    (

    ) =>
    {

    }
}
const req1
    =
    () =>
    function require() {}
let fn = req1()
const fs = fn("fs")
const path = fn("path")
console.log(path)
//
// fs.mkdir(path.join(__dirname, 'test'),(err) => {
//     console.log(err)
// })