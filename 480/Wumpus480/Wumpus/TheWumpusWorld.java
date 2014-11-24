import greenfoot.*;  // (World, Actor, GreenfootImage, Greenfoot and MouseInfo)
import java.util.Arrays;

/**
 * General class that represents a standard Wumpus World as described in ().
 * 
 * Due to draw constraints, minimum width is 8
 * 
 * @author Chris McKee 
 * @version Wumpus v1
 */
public class TheWumpusWorld extends World
{
    private static final int width = 8;
    private static final int cellSize = 60;
    private int[][] s1 = new int[width][width]; //Breeze
    private int[][] s2 = new int[width][width]; //Stench
    private int[][] pits = new int[width][width]; //Contains pit locations
    
    private Agent player;
    private Wumpus wumpy;
    private boolean daWumpusLives = false;
    private Other[] stenches = new Other[4];
    private Gold gold;
    private Other art;
    public Info score, sense1, sense2, goldInfo, bump, scream, arrows, death;
    private int arrowStart = 4;
    
    public TheWumpusWorld()
    {    
        // Create a new world with 10x10 cells with a cell size of 50x50 pixels.
        super(width + 6, width + 2, cellSize);
        score = new Info("Score: ", 10000);
        sense1 = new Info("Breeze: ", 0);
        sense2 = new Info("Stench: ", 0);
        goldInfo = new Info("Glitter: ", 0);
        bump = new Info("Bump: ", 0);
        scream = new Info("Scream: ", 0);
        arrows = new Info("Arrows Left: ", arrowStart);
        death = new Info("Dead: ", 0);
        populate();
    }
    
    public void act()
    {
        Greenfoot.delay(5);
        if(testForBreeze())
            sense1.setScore(1);
        else
            sense1.setScore(0);
        if(testForStench())
            sense2.setScore(1);
        else
            sense2.setScore(0);
        if(testForGlitter())
            goldInfo.setScore(1);
        else
            goldInfo.setScore(0);
            
        if(testForDeath())
            Greenfoot.stop();
    }
    
    private void populate() {
        addFrame();
        addInfo();
        addGold();
        addHazards();
        addPlayer();
    }
    
    private void addFrame()
    {
        //Build the map horizontals (top and bottom) first
        for(int i = 0; i < width + 6; i++)
        {
            art = new Other(cellSize, "wall");
            addObject(art, i, 0);
            art = new Other(cellSize, "wall");
            addObject(art, i, width + 1);
        }
        //then the vertical fillers
        for(int i = 1; i < width + 1; i++)
        {
            art = new Other(cellSize, "wall");
            addObject(art, 0, i);
            art = new Other(cellSize, "wall");
            addObject(art, width + 1, i);
            if(i == width/2 -3 || i == width/2 -2 || i == width/2 -1 || i == width/2 || i == width/2 +1 ||
                 i == width/2 +2 || i == width/2 +3 || i == width/2 +4)
            {}
            else
            {
                art = new Other(cellSize, "wall");
                addObject(art, width + 2, i);
                art = new Other(cellSize, "wall");
                addObject(art, width + 3, i);
                art = new Other(cellSize, "wall");
                addObject(art, width + 4, i);
            }
            art = new Other(cellSize, "wall");
            addObject(art, width + 5, i);
        }
    }
    
    private void addInfo()
    {
        addObject(score, width + 3, width/2 -3);
        addObject(sense1, width + 3, width/2 -2);
        addObject(sense2, width + 3, width/2-1);
        addObject(goldInfo, width + 3, width/2);
        addObject(bump, width + 3, width/2 +1);
        addObject(scream, width + 3, width/2 +2);
        addObject(arrows, width + 3, width/2 +3);
        addObject(death, width + 3, width/2 +4);
    }
    
    private void addPlayer()
    {
        player = new Agent(this);
        player.setArrowCount(arrowStart);
        addObject(player, 1, 1);
    }
    
    private void addHazard2(int i, int j)
    {
        art = new Other(cellSize, "pit");
        addObject(art, i, j);
        pits[i-1][j-1] = 1;
                        if(i > 1)
                        {
                            art = new Other(cellSize, "breeze");
                            addObject(art, i - 1, j);
                            s1[i-2][j-1] = 1;
                        }
                        if(i < width)
                        {
                            art = new Other(cellSize, "breeze");
                            addObject(art, i + 1, j);
                            s1[i][j-1] = 1;
                        }
                        if(j > 1)
                        {
                            art = new Other(cellSize, "breeze");
                            addObject(art, i, j - 1);
                            s1[i-1][j-2] = 1;
                        }
                        if(j < width)
                        {
                            art = new Other(cellSize, "breeze");
                            addObject(art, i, j + 1);
                            s1[i-1][j] = 1;
                        }

        art = new Other(cellSize, "cell");
        addObject(art, i, j);


    }
    
    private void addHazards()
    {
        int chanceForPit;
        addWumpus();
        for(int i = 1; i < width + 1; i++)
        {
            for(int j = 1; j < width + 1; j++)
            {
                if((i != 1 || j != 1) && ((i != gold.getX()) && (j != gold.getY())) 
                    && ((i != wumpy.getX()) && (j != wumpy.getY())))
                {
                    chanceForPit = Greenfoot.getRandomNumber(5);
                    if(chanceForPit == 1)
                    {
                        art = new Other(cellSize, "pit");
                        addObject(art, i, j);
                        pits[i-1][j-1] = 1;
                        if(i > 1)
                        {
                            art = new Other(cellSize, "breeze");
                            addObject(art, i - 1, j);
                            s1[i-2][j-1] = 1;
                        }
                        if(i < width)
                        {
                            art = new Other(cellSize, "breeze");
                            addObject(art, i + 1, j);
                            s1[i][j-1] = 1;
                        }
                        if(j > 1)
                        {
                            art = new Other(cellSize, "breeze");
                            addObject(art, i, j - 1);
                            s1[i-1][j-2] = 1;
                        }
                        if(j < width)
                        {
                            art = new Other(cellSize, "breeze");
                            addObject(art, i, j + 1);
                            s1[i-1][j] = 1;
                        }
                    }
                }
                art = new Other(cellSize, "cell");
                addObject(art, i, j);
            }
        }
    }
    
    private void addWumpus2(int x, int y)
    {
       
        wumpy = new Wumpus(cellSize * 9 / 10);
        
        while(true)
        {
            if((x != 1 || y != 1) && (x != gold.getX() && y != gold.getY()))
                break;
            else
            {
                x = Greenfoot.getRandomNumber(width) + 1;
                y = Greenfoot.getRandomNumber(width) + 1;
            }
        }
        addObject(wumpy, x, y);
        if(x > 1)
        {
            stenches[0] = new Other(cellSize, "stench");
            addObject(stenches[0], x - 1, y);
            s2[x-2][y-1] = 1;
        }
        if(x < width)
        {
            stenches[1] = new Other(cellSize, "stench");
            addObject(stenches[1], x + 1, y);
            s2[x][y-1] = 1;
        }
        if(y > 1)
        {
            stenches[2] = new Other(cellSize, "stench");
            addObject(stenches[2], x, y - 1);
            s2[x-1][y-2] = 1;
        }
        if(y < width)
        {
            stenches[3] = new Other(cellSize, "stench");
            addObject(stenches[3], x, y + 1);
            s2[x-1][y] = 1;
        }
        daWumpusLives = true;
    }
    
    
    
    private void addWumpus()
    {
        int x = Greenfoot.getRandomNumber(width) + 1;
        int y = Greenfoot.getRandomNumber(width) + 1;
        wumpy = new Wumpus(cellSize * 9 / 10);
        
        while(true)
        {
            if((x != 1 || y != 1) && (x != gold.getX() && y != gold.getY()))
                break;
            else
            {
                x = Greenfoot.getRandomNumber(width) + 1;
                y = Greenfoot.getRandomNumber(width) + 1;
            }
        }
        addObject(wumpy, x, y);
        if(x > 1)
        {
            stenches[0] = new Other(cellSize, "stench");
            addObject(stenches[0], x - 1, y);
            s2[x-2][y-1] = 1;
        }
        if(x < width)
        {
            stenches[1] = new Other(cellSize, "stench");
            addObject(stenches[1], x + 1, y);
            s2[x][y-1] = 1;
        }
        if(y > 1)
        {
            stenches[2] = new Other(cellSize, "stench");
            addObject(stenches[2], x, y - 1);
            s2[x-1][y-2] = 1;
        }
        if(y < width)
        {
            stenches[3] = new Other(cellSize, "stench");
            addObject(stenches[3], x, y + 1);
            s2[x-1][y] = 1;
        }
        daWumpusLives = true;
    }
    
    private void addGold()
    {
        int x = Greenfoot.getRandomNumber(width) + 1;
        int y = Greenfoot.getRandomNumber(width) + 1;
        gold = new Gold(cellSize);
        while(true)
        {
            if(x != 1 || y != 1)
                break;
            else
            {
                x = Greenfoot.getRandomNumber(width) + 1;
                y = Greenfoot.getRandomNumber(width) + 1;
            }
        }
        addObject(gold, x, y);
    }
    
    /*Returns the width of the playspace, as opposed to the built in getWidth() method,
     *  which will include the padding for the readout.
     */
    public int getPlayWidth()
    {
        return width;
    }
    
    public int getCellSize()
    {
        return cellSize;
    }
    
    public boolean testForBreeze()
    {
        return (s1[player.getX() - 1][player.getY() - 1] == 1);
    }
        
    public boolean testForStench()
    {
        return (s2[player.getX() - 1][player.getY() - 1] == 1);
    }
    
    public boolean testForGlitter()
    {
        if(player.getX() == gold.getX() && player.getY() == gold.getY())
            return true;
        else
            return false;
    }
    
    public boolean takeGold()
    {
        if(testForGlitter())
        {
            score.add(10000);
            removeObject(gold);
            score.updateImage();
            Greenfoot.stop();
        }
        return false;
    }
    
    public boolean testForDeath()
    {
        if(daWumpusLives == true && player.getX() == wumpy.getX() && player.getY() == wumpy.getY())
        {
            player.isAlive = false;
            death.setScore(1);
            return true;
        }
        else if(pits[player.getX() - 1][player.getY() - 1] == 1)
        {
            player.isAlive = false;
            death.setScore(1);
            return true;
        }
        else
        {
            death.setScore(0);
            return false;
        }
    }
    
    public boolean wallToThe(String direction)
    {
        if(direction.equals("NORTH"))
        {
            if(player.getY() == 1)
                return true;
        }
        else if(direction.equals("EAST"))
        {
            if(player.getX() == getPlayWidth())
                return true;
        }
        else if(direction.equals("SOUTH"))
        {
            if(player.getY() == getPlayWidth())
                return true;
        }
        else if(direction.equals("WEST"))
        {
            if(player.getX() == 1)
                return true;
        }
        return false;
    }
    
    public boolean checkTrajectory(String direction)
    {
        if(direction.equals("NORTH"))
        {
            if(player.getX() == wumpy.getX() && player.getY() > wumpy.getY())
                return true;
        }
        else if(direction.equals("EAST"))
        {
            if(player.getX() < wumpy.getX() && player.getY() == wumpy.getY())
                return true;
        }
        else if(direction.equals("SOUTH"))
        {
            if(player.getX() == wumpy.getX() && player.getY() < wumpy.getY())
                return true;
        }
        else if(direction.equals("WEST"))
        {
            if(player.getX() > wumpy.getX() && player.getY() == wumpy.getY())
                return true;
        }
        return false;
    }
    
    public void killWumpus()
    {
        this.removeObject(wumpy);
        daWumpusLives = false;
        for(int i = 0; i < 4; i++)
        {
            if(stenches[i] != null)
                this.removeObject(stenches[i]);
        }
        s2 = new int[width][width];
    }
}
