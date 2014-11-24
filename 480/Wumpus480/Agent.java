import greenfoot.*;  // (World, Actor, GreenfootImage, Greenfoot and MouseInfo)
import java.util.*;
/**
 * The agent will explore the wumpus world in search of the gold. They have at their displosal
 * a single arrow to kill the wumpus. They can also detect using 5 senses. This being:
 *    1) Detecting a glitter: The gold will glitter
 *    2) Detecting a breeze: Breezes appear in the directly adjacent blocks to a pit.
 *    3) Detecting a stench: The wumpus will put off a stench into the adjacent squares.
 *    4) Detecting a bump: Bumps occur when the agent attempts to walk beyond the confines of
 *       the world.
 *    5) Detecting a scream: If the agent fires his/her arrow forward into the wumpus, this will
 *       effectively slay the beast, causing it to let out a piercing cry.
 *       
 *    The agent has at his disposal these methods in order to determine their next move of action:
 *      *From the agent*
 *         *turnLeft(), turnRight() - turns the player in the direction indicated.
 *         *move() - advances the player one grid space forward in the direction they are currently
 *                    facing. This direction can also be checked within the private String heading,
 *                    which will indicate NORTH, EAST, WEST, or SOUTH.
 *         *senseBreeze(), senseStench(), senseGlitter() - these methods will return true if the
 *                    player is located on a space with the breeze, stench, or gold respectively.
 *         *shoot() - fires an arrow along the players current heading. If the wumpus is along said
 *                     heading, this method returns true to indicate a dead wumpus. UI will update 
 *                     display a scream heard. This decrements the arrow count if available, or
 *                     returns false if out of arrows. Remaining arrows are found in arrowsLeft.
 * 
 * @author Christopher McKee
 * @version W13
 */
public class Agent extends Actor
{
    private GreenfootImage foreground, eastImage, southImage, westImage, northImage;
    private TheWumpusWorld world;
    private String heading;
    private int arrowsLeft;
    public boolean isAlive;
    
    //Custom variables for the player to use while navigating
    private int[][] tracking;
    private boolean bumped, turning;   
    /* This method will be written by the student to include the logic needed by the agent.
     * As of now, it is has a very simple ai that is being used to show the use of the various
     * agent methods.
     */
    private class TrinhLocation implements Comparable<TrinhLocation>{
        public int x, y;
        public double distance, f_score = 0, g_score = 0;
        public TrinhLocation parent;
        public ArrayList<TrinhLocation> children;
        public TrinhLocation(int xx, int yy) {
            x = xx;
            y = yy;
        }
        
        public TrinhLocation(int xx, int yy, TrinhLocation par) {
            x = xx;
            y = yy;
            parent = par;
        }
        
        public void setParent(TrinhLocation l) {
            parent = l;
        }
        
        public TrinhLocation getParent() { return parent; }
        
        public void setChildren(ArrayList<TrinhLocation> children) {
            this.children = children;
        }
        
        public int compareTo(TrinhLocation loc) {
            return Double.compare(this.distance, loc.distance);
        }
        
        public double getFscore() { return f_score; }
        
        public double getGscore() { return g_score; }
        
        public void setGscore(double g_score) {
            this.g_score = g_score;
        }
        
        public void setFscore(double f_score) {
            this.f_score = f_score;
        }
        
        
    }
    private class TrinhTile {
        public boolean stench, breeze, glitter, possiblepit, pit, wumpus, safe, visited, blocked, risk;
        public int timesVisited = 0, pithit = 0;
        public TrinhLocation lastVisited;
        public void setStench(boolean b) {
            stench = b;
        }
        public void setVisited(boolean b) {
            visited = b;
        }
        public void setBreeze(boolean b) {
            breeze = b;
        }
        public void setPossiblePit(boolean b) {
            possiblepit = b;
        }
        public void setPit(boolean b) {
            pit = b;
        }
        public void setWumpus(boolean b) {
            wumpus = b;
        }
        public void setSafe(boolean b) {
            safe = b;
        }
    }
    boolean TrinhRiskMode = false;
    public class TrinhKB {
        private TrinhTile[][] kb = new TrinhTile[8][8]; 
        TrinhKB(int row, int col) {
            for (int i = 0; i < row; i++) { 
                for (int j = 0; j < col; j++) {
                    kb[i][j] = new TrinhTile();
                }
            }
        }
        public TrinhTile[][] getKB() {
            return kb;
        }
        
        public void setKB(TrinhTile[][] kb) {
            this.kb = kb;
        }
        
        public void updateKB(TrinhTile[][]kb) {
            for (int i = 0; i < 8; i++) {
                for (int j = 0; j < 8; j++) {
                    if (kb[i][j].breeze) {
                        tellKB(kb, "BreezeUpdate", new TrinhLocation(i, j));
                    }
                }
            }
        }
    }
    TrinhKB TrinhKB1 = new TrinhKB(8, 8); //World size is 8 assumed X IS ROW Y IS COLUMN
    private void printKB() {
        TrinhTile[][] kb = TrinhKB1.getKB();
        System.out.println("--------------");
        for (int i = 0; i < 8; i++) {
            for(int j = 0; j < 8; j++) {
                if (j == this.getX() - 1 && i == this.getY() - 1)
                    System.out.print("A  ");
                else if (!kb[j][i].visited && kb[j][i].safe)
                    System.out.print("U  ");
                else if (kb[j][i].breeze)
                    System.out.print("B  ");
                else if(kb[j][i].safe)
                    System.out.print("S  ");
                else if (kb[j][i].pit)
                    System.out.print("P  ");
                else if (kb[j][i].possiblepit)
                    System.out.print("M" + kb[j][i].pithit + " ");
                else
                    System.out.print("?  ");
                }
                System.out.println();
            }
            System.out.println("--------------");
        }
    private void tellKB(TrinhTile[][] kb, String str, TrinhLocation loc) {
        if (str.equals("Breeze") || str.equals("BreezeUpdate")) {
            kb[loc.x][loc.y].setSafe(true);
            kb[loc.x][loc.y].setBreeze(true);
            ArrayList<TrinhLocation> unsafeSpots = new ArrayList<TrinhLocation>();
            int xx = loc.x + 1;
            int yy = loc.y;
            if (xx < 8) {
                if (!kb[xx][yy].safe) {
                    unsafeSpots.add(new TrinhLocation(xx, yy));
                }
                /*
                if (kb[xx][yy].possiblepit == true && !kb[xx][yy].safe && kb[xx][yy].pithit > 2) {
                    kb[xx][yy].setPit(true);
                }
                else if (kb[xx][yy].safe != true) {
                    kb[xx][yy].pithit++;
                    kb[xx][yy].setPossiblePit(true);
                }
                */    
            }
            
            xx = loc.x;
            yy = loc.y + 1;
            
            if (yy < 8) {
                if (!kb[xx][yy].safe) {
                    unsafeSpots.add(new TrinhLocation(xx, yy));
                }
                /*
                if (kb[xx][yy].possiblepit == true && !kb[xx][yy].safe && kb[xx][yy].pithit > 2) {
                    kb[xx][yy].setPit(true);
                }
                else if (kb[xx][yy].safe != true) {
                    kb[xx][yy].pithit++;
                    kb[xx][yy].setPossiblePit(true);
                }
                */    
            }
            
            xx = loc.x;
            yy = loc.y - 1;
            
            if (yy >= 0) {
                if (!kb[xx][yy].safe) {
                    unsafeSpots.add(new TrinhLocation(xx, yy));
                }
                /*
                if (kb[xx][yy].possiblepit == true && !kb[xx][yy].safe && kb[xx][yy].pithit > 2) {
                    kb[xx][yy].setPit(true);
                }
                else if (kb[xx][yy].safe != true) {
                    kb[xx][yy].pithit++;
                    kb[xx][yy].setPossiblePit(true);
                }
                */    
            }
            
            xx = loc.x - 1;
            yy = loc.y;
            
            if (xx >= 0) {
                if (!kb[xx][yy].safe) {
                    unsafeSpots.add(new TrinhLocation(xx, yy));
                }
                /*
                if (kb[xx][yy].possiblepit == true && !kb[xx][yy].safe && kb[xx][yy].pithit > 2) {
                    kb[xx][yy].setPit(true);
                }
                else if (kb[xx][yy].safe != true) {
                    kb[xx][yy].pithit++;
                    kb[xx][yy].setPossiblePit(true);
                }
                */              
            }
            if (!unsafeSpots.isEmpty()) {
                if(unsafeSpots.size() == 1) {
                    TrinhLocation tmp = unsafeSpots.get(0);
                    kb[tmp.x][tmp.y].setPit(true);
                }
                else {
                    for (int i = 0; i < unsafeSpots.size(); i++) {
                        TrinhLocation tmp = unsafeSpots.get(i);
                        kb[tmp.x][tmp.y].possiblepit = true;
                        if (str.equals("Breeze") && !kb[loc.x][loc.y].visited)
                            kb[tmp.x][tmp.y].pithit += 1;
                    }
                }
            }
        }
        else if (str.equals("Nothing")) {
            int xx = loc.x + 1;
            int yy = loc.y;
            if (xx < 8) {
                kb[xx][yy].setSafe(true);        
            }
            
            xx = loc.x;
            yy = loc.y + 1;
            
            if (yy < 8) {
                kb[xx][yy].setSafe(true);      
            }
            
            xx = loc.x;
            yy = loc.y - 1;
            
            if (yy >= 0) {
                kb[xx][yy].setSafe(true);      
            }
            
            xx = loc.x - 1;
            yy = loc.y;
            
            if (xx >= 0) {
                kb[xx][yy].setSafe(true);               
            }
        }
        else if (str.equals("WumpusDied")) {
            if (heading.equals("EAST")) {
                loc.x = loc.x + 1;
            }
            else if (heading.equals("WEST")) {
                loc.x = loc.x - 1;
            }
            else if (heading.equals("NORTH")) {
                loc.y = loc.y - 1;
            }
            else if (heading.equals("SOUTH")) {
                loc.y = loc.y + 1;
            }
            kb[loc.x][loc.y].setSafe(true); 
            int xx = loc.x + 1;
            int yy = loc.y;
            if (xx < 8) {
                kb[xx][yy].setSafe(true);        
            }
            
            xx = loc.x;
            yy = loc.y + 1;
            
            if (yy < 8) {
                kb[xx][yy].setSafe(true);      
            }
            
            xx = loc.x;
            yy = loc.y - 1;
            
            if (yy >= 0) {
                kb[xx][yy].setSafe(true);      
            }
            
            xx = loc.x - 1;
            yy = loc.y;
            
            if (xx >= 0) {
                kb[xx][yy].setSafe(true);               
            }
            

        }
        printKB();
        
    }
    private double distance(TrinhLocation curr, TrinhLocation other) {
        double x2 = (double)other.x;
        double y2 = (double)other.y;
        double x = (double)curr.x;
        double y = (double)curr.y;
        return Math.sqrt(Math.pow((x2 - x), 2) + Math.pow((y2 - y), 2));
    }
    private Stack <TrinhLocation> generateActionPlan(TrinhTile[][] kb, TrinhLocation loc, boolean TrinhRiskMode) {
        PriorityQueue<TrinhLocation> unvisited = new PriorityQueue<TrinhLocation>();
        
        if (!TrinhRiskMode) {
            for(int i = 0; i < 8; i++) {
                for(int j = 0; j < 8; j++) {
                    if (!kb[i][j].visited && !kb[i][j].pit && !kb[i][j].possiblepit) {
                        TrinhLocation temp = new TrinhLocation(i, j);
                        temp.distance = distance(loc, temp);
                        unvisited.add(temp);
                    }
                }
            }
        }
        else {
            for(int i = 0; i < 8; i++) {
                for(int j = 0; j < 8; j++) {
                    if (!kb[i][j].visited && !kb[i][j].pit && kb[i][j].possiblepit) {
                        TrinhLocation temp = new TrinhLocation(i, j);
                        temp.distance = kb[i][j].pithit + Math.random();
                        unvisited.add(temp);
                        //System.out.println(temp.x + " " + temp.y);
                    }
                }
            }
            Iterator<TrinhLocation> it = unvisited.iterator(); 
            while(it.hasNext()) {
                TrinhLocation tmp2 = it.next();
                System.out.print("("+tmp2.x + "," + tmp2.y + ") ");
            }
        }
        
        Stack<TrinhLocation> path = new Stack<TrinhLocation>();
        while(!unvisited.isEmpty() && path.isEmpty()) {
           TrinhLocation goal = unvisited.remove();
           path.add(goal);
           //System.out.println("goal: " + goal.x + " " + goal.y);
           if (TrinhRiskMode) {
              System.out.println("Checking Minimum Risk Location " + "(" + goal.x + "," + goal.y + ")" );
              path = aStar(loc, goal, true); 
           }
           else {
               path = aStar(loc, goal, false);
           }
          if (path != null) {
               System.out.println("A* Action Plan found " + "to " + "(" + goal.x + "," + goal.y + ")");
               TrinhGoal = goal;
               return path;
           }
           else {
               path = new Stack<TrinhLocation>();
               //System.out.println("no path");
           }
        }
       return new Stack<TrinhLocation>();
    }
    
    public ArrayList<TrinhLocation> generateStates(TrinhLocation current) { 
        //{1, 0}, {0, 1}, {-1, 0}, {0, -1}, {1, 1}, {-1, -1}, {1, -1}, {-1, 1}
        ArrayList <TrinhLocation> list = new ArrayList<TrinhLocation>();
        int x = current.x;
        int y = current.y;
        list.add(new TrinhLocation(x + 1, y + 0, current));
        list.add(new TrinhLocation(x + 0, y + 1, current));
        list.add(new TrinhLocation(x - 1, y + 0, current));
        list.add(new TrinhLocation(x + 0, y - 1, current));
        current.setChildren(list);
        return list;
    }
    
    public boolean canMove(TrinhLocation loc) {
        TrinhTile[][] kb = TrinhKB1.getKB();
        TrinhTile tl;
        if (loc.x >= 0 && loc.x < 8 && loc.y >= 0 && loc.y < 8 ) {
            tl = kb[loc.x][loc.y];
        }
        else {
            return false;
        }
        if (tl.safe || (!tl.pit && !tl.possiblepit))          
            return true;  
        return false;
    }
    
    public boolean canMoveRisk(TrinhLocation loc, TrinhLocation goal) {
        TrinhTile[][] kb = TrinhKB1.getKB();
        TrinhTile tl;
        if (loc.x >= 0 && loc.x < 8 && loc.y >= 0 && loc.y < 8 ) {
            tl = kb[loc.x][loc.y];
        }
        else {
            return false;
        }
        if (tl.safe || !tl.pit || (tl.possiblepit && loc.x == goal.x && loc.y == goal.y))         
            return true;  
        return false;
    }
  public Stack<TrinhLocation> aStar(TrinhLocation start, TrinhLocation goal, boolean risk) {
        ArrayList <TrinhLocation> closedSet = new ArrayList<TrinhLocation>();
        PriorityQueue <TrinhLocation> openSet = new PriorityQueue<TrinhLocation>();
        start.setFscore(distance(start, goal));
        start.setGscore(0);
        openSet.add(start);
        
        while(openSet.size() > 0) {
            TrinhLocation current = openSet.poll();
             if(current.x == goal.x && current.y == goal.y) {

                 Stack <TrinhLocation> path = new Stack<TrinhLocation>();
                 while (current != null) {
                     path.push(current);
                     current = current.getParent();
                 }
                 
                 return path;
             }
            closedSet.add(current);
            for (TrinhLocation loc : generateStates(current)) {
                if (!risk) {
                    if (canMove(loc)) {
                        boolean skip = false;
                        for (int i = 0; i < closedSet.size(); i++) {
                            TrinhLocation tmp = closedSet.get(i);
                            if (tmp.x == loc.x && tmp.y == loc.y) {
                                skip = true;
                                break;
                            }
                        }
                        if (skip) {
                            continue;
                        }
                        skip = false;
                        double tent_g_score = current.getGscore() + distance(current, loc);
                        
                        
                        if (!openSet.contains(loc) || (loc.getGscore() >= 0 && tent_g_score < loc.getGscore())) {
                            loc.setGscore(tent_g_score);
                            loc.setFscore(loc.getGscore() + distance(loc, goal));
                            
                            Iterator<Agent.TrinhLocation> it = openSet.iterator();
                            while (it.hasNext()) {
                                TrinhLocation tmp = it.next();
                                if (tmp.x == loc.x && tmp.y == loc.y) {
                                    skip = true;
                                }
                            }
                            if (!skip) {
                                openSet.add(loc);
                            }
                        }
     
                    }
                }
                else {
                    if (canMoveRisk(loc, goal)) {
                        boolean skip = false;
                        for (int i = 0; i < closedSet.size(); i++) {
                            TrinhLocation tmp = closedSet.get(i);
                            if (tmp.x == loc.x && tmp.y == loc.y) {
                                skip = true;
                                break;
                            }
                        }
                        if (skip) {
                            continue;
                        }
                        skip = false;
                        double tent_g_score = current.getGscore() + distance(current, loc);
                        
                        
                        if (!openSet.contains(loc) || (loc.getGscore() >= 0 && tent_g_score < loc.getGscore())) {
                            loc.setGscore(tent_g_score);
                            loc.setFscore(loc.getGscore() + distance(loc, goal));
                            
                            Iterator<Agent.TrinhLocation> it = openSet.iterator();
                            while (it.hasNext()) {
                                TrinhLocation tmp = it.next();
                                if (tmp.x == loc.x && tmp.y == loc.y) {
                                    skip = true;
                                }
                            }
                            if (!skip) {
                                openSet.add(loc);
                            }
                        }
     
                    }
                }
            }         
        }
        //System.out.println("atar Returning null");
        return null;
    }
    Stack<TrinhLocation> Trinhlocations = new Stack<TrinhLocation>();
    boolean TrinhnowTurning = false;
    TrinhLocation TrinhGoal;
    private TrinhLocation findNextMove(TrinhTile[][] kb, TrinhLocation loc) {
        
        TrinhTile current = kb[loc.x][loc.y];
        if (!Trinhlocations.isEmpty()) {
            
            TrinhLocation newl = Trinhlocations.pop();
            if(kb[newl.x][newl.y].safe && !TrinhRiskMode) {
                return newl;
            }
            else if (kb[newl.x][newl.y].safe && TrinhRiskMode) {
                System.out.println("Following a risky path...");
                Iterator<TrinhLocation> it = Trinhlocations.iterator(); 
                if (it.hasNext()) {
                    if (!kb[newl.x][newl.y].safe && kb[newl.x][newl.y].possiblepit && newl.x != TrinhGoal.x && newl.y != TrinhGoal.y) {
                        Trinhlocations.clear();
                    }
                }
                if (newl.x == TrinhGoal.x && newl.y == TrinhGoal.y) {
                    TrinhRiskMode = false;
                }
                it = Trinhlocations.iterator();
                System.out.println("Next risk locations: ");
                while(it.hasNext()) {
                    TrinhLocation tmp2 = it.next();
                    System.out.print("("+tmp2.x + "," + tmp2.y + ") ");                
                }
                
                
                return newl;
            }
            else {
                Trinhlocations.clear(); //worthless and needs to be reupdated
            }
        }
            
        int xx = loc.x + 1;
        int yy = loc.y;
        if (xx < 8) {
            if (kb[xx][yy].safe && !kb[xx][yy].visited) {
                return new TrinhLocation(xx,yy);
            }
        }
            
        xx = loc.x;
        yy = loc.y + 1;
            
        if (yy < 8) {
            if (kb[xx][yy].safe && !kb[xx][yy].visited) {
                return new TrinhLocation(xx,yy);
            }  
        }
            
        xx = loc.x;
        yy = loc.y - 1;
            
        if (yy >= 0) {
            if (kb[xx][yy].safe && !kb[xx][yy].visited) {
                return new TrinhLocation(xx,yy);
            }  
        }
            
        xx = loc.x - 1;
        yy = loc.y;
            
        if (xx >= 0) {
            if (kb[xx][yy].safe && !kb[xx][yy].visited) {
                return new TrinhLocation(xx,yy);
            }               
        }
        
        System.out.println("all safe unvisited tiles visited, generating plan w/ A* search");
        Trinhlocations = generateActionPlan(kb, loc, false);
        if(!Trinhlocations.isEmpty()) {
            //System.out.println("Stack Size" + " " + stk.size());
            if (Trinhlocations.size() > 1) {
                Trinhlocations.pop();
                return Trinhlocations.pop();
            }
        }
        /*
        Stack<TrinhLocation> stk =  generateActionPlan(kb, loc);
        if(!stk.isEmpty()) {
            System.out.println("Stack Size" + " " + stk.size());
            if (stk.size() > 1) {
                stk.pop();
                return stk.pop();
            }

        }*/
         //take risk
        System.out.println("TAKING RISK");
        TrinhRiskMode = true;
        Trinhlocations = generateActionPlan(kb, loc, true);
        if(!Trinhlocations.isEmpty()) {
            //System.out.println("Stack Size" + " " + stk.size());
            if (Trinhlocations.size() > 1) {
                Trinhlocations.pop();
                return Trinhlocations.pop();
            }
        }else {
            return null;
        }
         return null;
    }
    private void checkDirection(TrinhLocation next) {
        int myX = this.getX();
        int myY = this.getY();
        int nextX = next.x + 1;
        int nextY = next.y + 1;
        if (nextX - myX > 0) { // >>
            if (heading.equals("EAST")) {
                TrinhnowTurning = false;
            }
        }
        else if (nextX - myX < 0) { // <<
            if (heading.equals("WEST")) {
                TrinhnowTurning = false;
            }
        }
        else if (nextY - myY > 0) {
            if (heading.equals("SOUTH")) {
                TrinhnowTurning = false;
            }
            
        }
        else if (nextY - myY < 0) {
            if (heading.equals("NORTH")) {
                TrinhnowTurning = false;
            }
           
        }
    }
    
    private void changeDirection(TrinhLocation next) {
        int myX = this.getX();
        int myY = this.getY();
        int nextX = next.x + 1;
        int nextY = next.y + 1;
        if (nextX - myX > 0) { // >>
            if (heading.equals("NORTH")) {
                this.turnRight();
            }
            else if (heading.equals("WEST")) {
                this.turnRight();
            }
            else if (heading.equals("SOUTH")){
                this.turnLeft();
            }
        }
        else if (nextX - myX < 0) { // <<
            if (heading.equals("EAST")) {
                this.turnLeft();
            }
            else if (heading.equals("NORTH")) {
                this.turnLeft();
            }
            else if (heading.equals("SOUTH")) {
                this.turnRight();
            }
        }
        else if (nextY - myY > 0) {
            if (heading.equals("NORTH")) {
                this.turnLeft();
            }
            else if (heading.equals("EAST")) {
                this.turnRight();
            }
            else if (heading.equals("WEST")) {
                this.turnLeft();
            }
        }
        else if (nextY - myY < 0) {
            if (heading.equals("SOUTH")) {
                this.turnRight();
            }
            else if (heading.equals("EAST")) {
                this.turnLeft();
            }
            else if (heading.equals("WEST")) {
                this.turnRight();
            }
        }
    }
    TrinhLocation next = null;
    boolean nextMove = false;
    private void makeNextMove()
    {
        //senseGlitter detects if you are on the gold
        
        TrinhTile[][] kb = TrinhKB1.getKB();
        TrinhKB1.updateKB(kb);
        if (TrinhnowTurning) {
            changeDirection(next);
            checkDirection(next);
            if (!TrinhnowTurning) {
                nextMove = true;
            }
        }
        else if (nextMove) {
            this.move();
            nextMove = false;
        }
        else {
            
            if(this.senseGlitter() == true)
            {
                world.takeGold();
            }
            //senseStench detects if you are currently adjacent to the wumpus
            else if(this.senseStench() == true)
            {
                tellKB(kb, "Stench", new TrinhLocation(this.getX() - 1, this.getY() - 1));
                //shoot fires the arrow along your current heading, returning true on a hit
                while(this.shoot() == false)
                    this.turnLeft();
                tellKB(kb, "WumpusDied", new TrinhLocation(this.getX() - 1, this.getY() - 1)); 
            }
            //senseBreeze detects if you are adjacent to a pit
            //bumped indicates if you previously failed to move forward
            //turning indicates if you previously rotated your agent
            else if(this.senseBreeze() == true) {
                tellKB(kb, "Breeze", new TrinhLocation(this.getX() - 1, this.getY() - 1));
            }
            else
            {
            //player moves forward one space, if this 
                tellKB(kb, "Nothing", new TrinhLocation(this.getX() - 1, this.getY() - 1));
                /*if(this.move() == false)
                    bumped = true;
                else
                    bumped = false;
            
                turning = false;*/
            }
            kb[this.getX() - 1][this.getY() - 1].visited = true;
            kb[this.getX() - 1][this.getY() - 1].safe = true;
            next = findNextMove(kb, new TrinhLocation(this.getX() - 1, this.getY() - 1));
            TrinhnowTurning = true;
            checkDirection(next);
            if (TrinhnowTurning == false) {
                this.move();
            }
            kb[next.x][next.y].lastVisited = new TrinhLocation(this.getX() - 1, this.getY() - 1);
        }
    }
   
    
    /**************************************************************************************/
    
    
    public Agent(TheWumpusWorld playSpace)
    {
        int size;
        world = playSpace;
        tracking = new int[world.getPlayWidth()][world.getPlayWidth()];
        eastImage = new GreenfootImage("AgentEast.png");
        southImage = new GreenfootImage("AgentSouth.png");
        westImage = new GreenfootImage("AgentWest.png");
        northImage = new GreenfootImage("AgentNorth.png");
        size = world.getCellSize() * 9 / 10;
        eastImage.scale(size, size);
        southImage.scale(size, size);
        westImage.scale(size, size);
        northImage.scale(size, size);
        heading = "EAST";
        foreground = eastImage;
        setImage(foreground);
        isAlive = true;
        
        //Initialize your custom variables
        bumped = turning = false;
    }
    /**
     * Act - do whatever the Agent wants to do. This method is called whenever
     * the 'Act' or 'Run' button gets pressed in the environment.
     */
    public void act() 
    {
        if(isAlive == true)
            makeNextMove();
            
        world.score.updateImage();
    }
    
    private void turnLeft()
    {
        world.bump.setScore(0);
        if(heading.equals("NORTH"))
        {
            heading = "WEST";
            foreground = westImage;
        }
        else if(heading.equals("EAST"))
        {
            heading = "NORTH";
            foreground = northImage;
        }
        else if(heading.equals("SOUTH"))
        {
            heading = "EAST";
            foreground = eastImage;
        }
        else if(heading.equals("WEST"))
        {
            heading = "SOUTH";
            foreground = southImage;
        }
        setImage(foreground);
        world.score.subtract(10);
    }
    
    private void turnRight()
    {
        world.bump.setScore(0);
        if(heading.equals("NORTH"))
        {
            heading = "EAST";
            foreground = eastImage;
        }
        else if(heading.equals("EAST"))
        {
            heading = "SOUTH";
            foreground = southImage;
        }
        else if(heading.equals("SOUTH"))
        {
            heading = "WEST";
            foreground = westImage;
        }
        else if(heading.equals("WEST"))
        {
            heading = "NORTH";
            foreground = northImage;
        }
        setImage(foreground);
        world.score.subtract(10);
    }
    
    private boolean move()
    {
        world.bump.setScore(0);
        if(world.wallToThe(heading))
        {
            world.bump.setScore(1);
            world.score.subtract(20);
            return false;
        }
        else
        {
            if(heading.equals("NORTH"))
                setLocation(getX(), getY() - 1);
            else if(heading.equals("EAST"))
                setLocation(getX() + 1, getY());
            else if(heading.equals("SOUTH"))
                setLocation(getX(), getY() + 1);
            else if(heading.equals("WEST"))
                setLocation(getX() - 1, getY());
        }
        
        if(world.testForDeath()) {
            world.score.subtract(1000);
        }
        else {
            world.score.subtract(20);
        }
            
        return true;
    }
    
    private boolean senseBreeze()
    {
        world.score.subtract(1);
        return world.testForBreeze();
    }
    
    private boolean senseStench()
    {
        world.score.subtract(1);
        return world.testForStench();
    }
    
    private boolean senseGlitter() 
    {
        world.score.subtract(1);
        return world.testForGlitter();
    }
    
    private boolean shoot()
    {
        world.bump.setScore(0);
        if(arrowsLeft > 0)
        {
            Arrow shot = new Arrow(world, heading);
            world.addObject(shot, getX(), getY());
            world.arrows.setScore(--arrowsLeft);
            world.score.subtract(20);
            if(world.checkTrajectory(heading))
            {
                world.killWumpus();
                world.scream.setScore(1);
                return true;
            }
        }
        world.scream.setScore(0);
        return false;
    }
    
    public void setArrowCount(int count)
    {
        this.arrowsLeft = count;    
    }
}
