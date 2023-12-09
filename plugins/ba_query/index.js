import { init, dec } from "./runnable.js"

await init()

// function decrypt(data) {
//   return dec(data)
// }

console.log(dec(process.argv[2]));

// init().then(() => {
//   console.log("listLast", decrypt("6vGRbnhOXIDmmF1HYbbUOz37OarY1/+uJkV4kef5PuKxHRgxtfIATGiXtTph0h7OUENGU65qHVzmWsxEmOjnZdZlQUPG2Z9kuWf7K+nwXxmi7jKyK/tBtXuUyhj+FGr8G4kJ3ZBlPFV+b7+xOT9WcewoZ4QNQCBFf0sMg/o4auHucMzCD2wYdqwfs7jGVxWCtqVLPs5ELnO/rxPIKID6YrqG/ClOPGxg5CHzNAD5cdY="));
// })
// console.log(decrypt("6vGRbnhOXIDmmF1HYbbUOz37OarY1/+uJkV4kef5PuKxHRgxtfIATGiXtTph0h7OUENGU65qHVzmWsxEmOjnZdZlQUPG2Z9kuWf7K+nwXxmi7jKyK/tBtXuUyhj+FGr8G4kJ3ZBlPFV+b7+xOT9WcewoZ4QNQCBFf0sMg/o4auHucMzCD2wYdqwfs7jGVxWCtqVLPs5ELnO/rxPIKID6YrqG/ClOPGxg5CHzNAD5cdY="));
