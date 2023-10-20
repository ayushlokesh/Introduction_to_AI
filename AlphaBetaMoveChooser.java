import java.util.ArrayList;

/**
 * Solution code for Comp24011 Reversi lab
 *
 * @author USERNAME
 */

public class AlphaBetaMoveChooser extends MoveChooser {
    /**
     * MoveCooser implementation AlphaBetaMoveChooser(int)
     *
     * @param   searchDepth The requested depth for minimax search
     */
    public AlphaBetaMoveChooser(int searchDepth) {
        // Add object initialisation code...
        super("MyAwesomeAgent",searchDepth);
    }

    /**
     * Need to implement chooseMove(BoardState,Move)
     *
     * @param   boardState  The current state of the game board
     *
     * @param   hint        Skip move or board location clicked on the UI
     *                      This parameter should be ignored!
     *
     * @return  The move chosen by alpha-beta pruning as discussed in the course
     */
    public Move chooseMove(BoardState boardState, Move hint) {
        // Add alpha-beta pruning code...
        Move ans= null; int val=0, x = 0;
         ArrayList<Move> l = boardState.getLegalMoves(); int alpha = -200000, beta = 200000;
        if(boardState.colour < 0){ val = 200000;
        for(Move m : l){
            x = maxMove(boardState.deepCopy(),m,1, alpha, beta);
            if (x < val){
                val = x; beta = Math.min(beta,x);
                ans = m;
            }
        }} 
        else if (boardState.colour > 0){val = -2000000;
            for(Move m : l){
            x = minMove(boardState.deepCopy(),m,1, alpha, beta);
            if (x > val){
                val = x; alpha = Math.max(alpha,x);
                ans = m;}}}
        return ans;
    }
    private int maxMove(BoardState b, Move m1, int d, int alpha, int beta){
        int val = -200000, x = 0;
        b.makeLegalMove(m1);
        if(d < this.searchDepth && !b.gameOver()){
            ArrayList<Move> l = b.getLegalMoves();
            for(Move m : l){
                x = minMove(b.deepCopy(), m,d+1,alpha, beta);
                
                val = Math.max(x,val); 
                alpha = Math.max(alpha,x);
                if(val >= beta){
                    return val;
                }
                
            } return val;}
        return boardEval(b);
    }

    private int minMove(BoardState b, Move m1, int d, int alpha, int beta){
        int val = 200000, x = 0;
        b.makeLegalMove(m1);
        if(d < this.searchDepth && !b.gameOver()){
            ArrayList<Move> l = b.getLegalMoves();
            for(Move m : l){
                x = maxMove(b.deepCopy(), m,d+1, alpha, beta);
                
                val = Math.min(x,val);
                beta = Math.min(beta,x); 
                if(val <= alpha){
                    return val;
                }
                
            } return val;}
        return boardEval(b);
    } 

    /**
     * Need to implement boardEval(BoardState)
     *
     * @param   boardState  The current state of the game board
     *
     * @return  The value of the board using Norvig's weighting of squares
     */
    public int boardEval(BoardState boardState) {
        // Add board evaluation code...
        int ans= 0;
        int[][] board = {
            {120, -20, 20, 5, 5, 20, -20, 120},
            {-20, -40, -5, -5, -5, -5, -40, -20},
            {20, -5, 15, 3, 3, 15, -5, 20},
            {5, -5, 3, 3, 3, 3, -5, 5},
            {5, -5, 3, 3, 3, 3, -5, 5},
            {20, -5, 15, 3, 3, 15, -5, 20},
            {-20, -40, -5, -5, -5, -5, -40, -20},
            {120, -20, 20, 5, 5, 20, -20, 120}
        };
        for(int i = 0; i < 4; i++){
            for(int j = 0; j < 4; j++){ 
                ans += board[i][j]*(boardState.getContents(i, j) + boardState.getContents(7-i, 7-j)
                + boardState.getContents(7-i, j) + boardState.getContents(i, 7-j));

            }
        }
        return ans;
    }

}

/* vim:set et ts=4 sw=4: */
