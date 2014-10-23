import greenfoot.*;  // imports Actor, World, Greenfoot, GreenfootImage

import java.util.List;
import java.util.ArrayList;
import java.util.PriorityQueue;
import java.util.Stack;

/**
 * Wombat. A Wombat moves forward until it can't do so anymore, at
 * which point it turns left. This wombat can not move over rocks. 
 * If a wombat finds a leaf, it eats it.
 * 
 * @author Michael Kolling
 * @version 1.0.1
 */
public class Wombat extends Actor
{
    private static final int EAST = 0;
    private static final int WEST = 1;
    private static final int NORTH = 2;
    private static final int SOUTH = 3;

    private int direction;
    private int leavesEaten;
    
    private GreenfootImage wombatRight;
    private GreenfootImage wombatLeft;
    private Stack<Location> path;
    
    private class Location implements Comparable<Location> {
        private int x, y;
        private double f_score, g_score = -1;
        private Location parent;
        private ArrayList<Location> children; 
        public Location(int x, int y, int heuristic, Location parent) {
            this.x = x;
            this.y = y;
            this.f_score = f_score;
            this.parent = parent;
            this.children = new ArrayList<Location>();
        }
        
        public void addChild(Location child) {
            children.add(child);
        }
        
        public void setChildren(ArrayList<Location> children) {
            this.children = children;
        }
        
        public ArrayList<Location> getChildren () { return children; }
        
        public int getX() { return x; }
        
        public int getY() { return y; }
        
        public double getFscore() { return f_score; }
        
        public double getGscore() { return g_score; }
        
        public void setGscore(double g_score) {
            this.g_score = g_score;
        }
        
        public void setFscore(double f_score) {
            this.f_score = f_score;
        }
        
        public int compareTo(Location loc) {
            return Double.compare(this.f_score, loc.getFscore());
        }
        
        public void setParent(Location l) {
            parent = l;
        }
        
        public Location getParent() { return parent; }
        
        public boolean equals(Location l) {
            return l.getX() == this.x && l.getY() == this.y;
        }
    }
    
    public Wombat()
    {
        wombatRight  = getImage();
        wombatLeft = new GreenfootImage(getImage());
        wombatLeft.mirrorHorizontally();
        
        setDirection(EAST);
        leavesEaten = 0;
    }

    /**
     * Do whatever the wombat likes to to just now.
     */
    public void act()
    {
        if (path == null) {
            path = aStar();
        }
        
        if(foundLeaf()) {
            eatLeaf();
        }
        else {
            if (!path.empty()) {
                Location loc = path.pop();
                setLocation((int)loc.getX(), (int)loc.getY());
            }
        }
        
    }

    /**
     * Check whether there is a leaf in the same cell as we are.
     */
    public boolean foundLeaf()
    {
        Actor leaf = getOneObjectAtOffset(0, 0, Leaf.class);
        if(leaf != null) {
            return true;
        }
        else {
            return false;
        }
    }
    
    /**
     * Eat a leaf.
     */
    public void eatLeaf()
    {
        Actor leaf = getOneObjectAtOffset(0, 0, Leaf.class);
        if(leaf != null) {
            // eat the leaf...
            getWorld().removeObject(leaf);
            leavesEaten = leavesEaten + 1; 
        }
    }
    
    /**
     * Move one cell forward in the current direction.
     */
    public void move()
    {
        int targetX = ((WombatWorld) getWorld()).theLeaf.getX();
        int targetY = ((WombatWorld) getWorld()).theLeaf.getY();
        
        if (!canMove()) {
            return;
        }
        switch(direction) {
            case SOUTH :
                setLocation(getX(), getY() + 1);
                break;
            case EAST :
                setLocation(getX() + 1, getY());
                break;
            case NORTH :
                setLocation(getX(), getY() - 1);
                break;
            case WEST :
                setLocation(getX() - 1, getY());
                break;
        }
    }

    /**
     * Test if we can move forward. Return true if we can, false otherwise.
     */
    public boolean canMove()
    {
        World myWorld = getWorld();
        int x = getX();
        int y = getY();
        switch(direction) {
            case SOUTH :
                y++;
                break;
            case EAST :
                x++;
                break;
            case NORTH :
                y--;
                break;
            case WEST :
                x--;
                break;
        }
        // test for outside border
        if (x >= myWorld.getWidth() || y >= myWorld.getHeight()) {
            return false;
        }
        else if (x < 0 || y < 0) {
            return false;
        }
        List rocks = myWorld.getObjectsAt(x, y, Rock.class);
        if(rocks.isEmpty()) {
            return true;
        }
        else {
            return false;
        }
    }
    
    public boolean canMove(Location loc) {
        World myWorld = getWorld();
        int x = loc.getX();
        int y = loc.getY();
        
        
        if (x >= myWorld.getWidth() || y >= myWorld.getHeight()) {
            return false;
        }
        else if (x < 0 || y < 0) {
            return false;
        }
        List rocks = myWorld.getObjectsAt(x, y, Rock.class);
        if(rocks.isEmpty()) {
            return true;
        }
        else {
            return false;
        }
    }
    
    public double Heuristic(Location loc, Location loc2) {
        double x2 = (double)loc2.getX();
        double y2 = (double)loc2.getY();
        double x = (double)loc.getX();
        double y = (double)loc.getY();
        return Math.sqrt(Math.pow((x2 - x), 2) + Math.pow((y2 - y), 2));
        
    }
    
    public ArrayList<Location> generateStates(Location current) { 
        //{1, 0}, {0, 1}, {-1, 0}, {0, -1}, {1, 1}, {-1, -1}, {1, -1}, {-1, 1}
        ArrayList <Location> list = new ArrayList<Location>();
        int x = current.getX();
        int y = current.getY();
        list.add(new Location(x + 1, y + 0, 0, current));
        list.add(new Location(x + 0, y + 1, 0, current));
        list.add(new Location(x - 1, y + 0, 0, current));
        list.add(new Location(x + 0, y - 1, 0, current));
        list.add(new Location(x + 1, y + 1, 0, current));
        list.add(new Location(x - 1, y - 1, 0, current));
        list.add(new Location(x + 1, y - 1, 0, current));
        list.add(new Location(x - 1, y + 1, 0, current));
        current.setChildren(list);
        return list;
    }
    
    public Stack<Location> aStar() {
        ArrayList <Location> closedSet = new ArrayList<Location>();
        PriorityQueue <Location> openSet = new PriorityQueue<Location>();
     
        Location start = new Location(getX(), getY(), 0, null);
        Location goal = new Location(((WombatWorld) getWorld()).theLeaf.getX(), ((WombatWorld) getWorld()).theLeaf.getY(), 0, null);
        start.setFscore(Heuristic(start, goal));
        start.setGscore(0);
        openSet.add(start);
        
        while(openSet.size() > 0 ) {
            Location current = openSet.poll();
            
             if(current.getX() == goal.getX() && current.getY() == goal.getY()) {

                 Stack <Location> path = new Stack<Location>();
                 while (current != null) {
                     path.push(current);
                     current = current.getParent();
                 }
                 
                 return path;
             }
            closedSet.add(current);
            for (Location loc : generateStates(current)) {
                if (canMove(loc)) {
                    if (closedSet.contains(loc)) {
                        continue;
                    }
                    double tent_g_score = current.getGscore() + Heuristic(current, loc);
                    
                    
                    if (!openSet.contains(loc) || (loc.getGscore() >= 0 && tent_g_score < loc.getGscore())) {
                        loc.setGscore(tent_g_score);
                        loc.setFscore(loc.getGscore() + Heuristic(loc, goal));
                        if (!openSet.contains(loc)) {
                            openSet.add(loc);
                        }
                    }
 
                }
            }                     
        }
        return null;
    }
    
    /**
     * Turn in a random direction.
     */
    public void turnRandom()
    {
        // get a random number between 0 and 3...
        int turns = Greenfoot.getRandomNumber(4);
        
        // ...an turn left that many times.
        for(int i=0; i<turns; i++) {
            turnLeft();
        }
        
        
    }

    /**
     * Turns towards the left.
     */
    public void turnLeft()
    {
        switch(direction) {
            case SOUTH :
                setDirection(EAST);
                break;
            case EAST :
                setDirection(NORTH);
                break;
            case NORTH :
                setDirection(WEST);
                break;
            case WEST :
                setDirection(SOUTH);
                break;
        }
    }

    /**
     * Sets the direction we're facing.
     */
    public void setDirection(int direction)
    {
        this.direction = direction;
        switch(direction) {
            case SOUTH :
                setImage(wombatRight);
                setRotation(90);
                break;
            case EAST :
                setImage(wombatRight);
                setRotation(0);
                break;
            case NORTH :
                setImage(wombatLeft);
                setRotation(90);
                break;
            case WEST :
                setImage(wombatLeft);
                setRotation(0);
                break;
            default :
                break;
        }
    }

    /**
     * Tell how many leaves we have eaten.
     */
    public int getLeavesEaten()
    {
        return leavesEaten;
    }
}