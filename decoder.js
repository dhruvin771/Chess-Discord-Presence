import { tcnToPgn } from "chess-tcn";

const tcn = process.argv[2];

try {
    const pgn = tcnToPgn(tcn);
    console.log(pgn);
} catch (err) {
    console.error(err);
    process.exit(1);
}