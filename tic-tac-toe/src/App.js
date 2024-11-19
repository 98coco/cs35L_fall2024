// Chorus Lapilli

import { useState } from 'react';

function Square({value ,onSquareClick}) {
  return <button className="square" onClick = {onSquareClick}>{value}</button>;
}

export default function Board() {
  const [xIsNext, setXIsNext] = useState(true);
  const [squares, setSquares] = useState(Array(9).fill(null));
  const [movePiece, setMovePiece] = useState(null);

  let xCount = 0;
  let oCount = 0;
  for (let i = 0; i< squares.length; i++){ //helps check to make sure only 3 pieces are on the board 
    if (squares[i] == "X"){
      xCount++
    }
    else if (squares[i] == "O"){
      oCount++
    }
  }

  function handleClick(i) {
    if (calculateWinner(squares)) { //returns early if there is something on that square 
      return;
    }

    const nextSquares = squares.slice();

    if (xIsNext && xCount === 3){
      if(squares[i] === "X"){
        setMovePiece(i) //first click, log this index
      }
      else if (isValidMove(movePiece,i,nextSquares,"X")){ //second click valid
        nextSquares[movePiece] = null
        nextSquares[i] = "X"
        setSquares(nextSquares)
        setMovePiece(null)
        setXIsNext(!xIsNext)
        return;
      }
      return 
    }
    
    if (!xIsNext && oCount === 3){
      if(squares[i] === "O"){
        setMovePiece(i) //first click, log this index
      }
      else if (isValidMove(movePiece,i,nextSquares,"O")){ //second click valid
        console.log('inside isvalid move');
        nextSquares[movePiece] = null
        nextSquares[i] = "O"
        setSquares(nextSquares)
        setMovePiece(null)
        setXIsNext(!xIsNext)
        return;
      }
      return 
    }

    if (squares[i]){
      return;
    }

    if (xIsNext) {
      nextSquares[i] = "X";
    } else {
      nextSquares[i] = "O";
    }
    setSquares(nextSquares);
    setXIsNext(!xIsNext);
  }

  const winner = calculateWinner(squares);
  let status;
  if (winner) {
    status = "Winner: " + winner;
  } else {
    status = "Next player: " + (xIsNext ? "X" : "O"); //if xIsNext , next player is X, else it is O
  }

  return (
    <>
      <div className="status">{status}</div>
      <div>replacing index: {movePiece}</div>
      <div className="board-row">
        <Square value={squares[0]} onSquareClick={() => handleClick(0)} />
        <Square value={squares[1]} onSquareClick={() => handleClick(1)} />
        <Square value={squares[2]} onSquareClick={() => handleClick(2)} />
      </div>
      <div className="board-row">
        <Square value={squares[3]} onSquareClick={() => handleClick(3)} />
        <Square value={squares[4]} onSquareClick={() => handleClick(4)} />
        <Square value={squares[5]} onSquareClick={() => handleClick(5)} />
      </div>
      <div className="board-row">
        <Square value={squares[6]} onSquareClick={() => handleClick(6)} />
        <Square value={squares[7]} onSquareClick={() => handleClick(7)} />
        <Square value={squares[8]} onSquareClick={() => handleClick(8)} />
      </div>
    </>
  );
}

function isValidMove (currIndex,moveIndex,squares,player){ //checks to see if the second move is a valid move --> call this function on the second click
  const possibleMoves ={ // 0:,1:....8: are the keys --> possible moves are the indexs in the list 
    0:[1,3,4],
    1:[0,2,3,4,5],
    2:[1,4,5],
    3:[0,1,4,6,7],
    4:[0,1,2,3,5,6,7,8],
    5:[1,2,4,7,8],
    6:[3,4,7],
    7:[3,4,5,6,8],
    8:[4,5,7]
  }; 
  let check = possibleMoves[currIndex].includes(moveIndex); //finds the key of curr index, then checks to see if the index they want to move to is a valid box from that curr index

  if (check && squares[4] == player && currIndex !== 4){ //player occupies the center 
    squares[currIndex] = null
    squares[moveIndex] = player
    return calculateWinner(squares);
  }

  if (check && squares[moveIndex] == null){
    return true
  }
  else{
    return false
  }

}

function calculateWinner (squares) {
  const lines = [
    [0, 1, 2],  //top row
    [3, 4, 5],  //middle row
    [6, 7, 8],  //bottom row
    [0, 3, 6],  //left column
    [1, 4, 7],  //middle column
    [2, 5, 8],  //right column
    [0, 4, 8],  //diagonal (top-left to bottom-right)
    [2, 4, 6]   //diagonal (top-right to bottom-left)
  ]; //refers to the possibilities of where a winner can win

  for (let i = 0; i < lines.length; i++) {
    const [a, b, c] = lines[i];
    if (squares[a] && squares[a] === squares[b] && squares[a] === squares[c]) {
      return squares[a];
    }
  }
  return null;
}