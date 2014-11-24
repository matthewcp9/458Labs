import greenfoot.*;  // (World, Actor, GreenfootImage, Greenfoot and MouseInfo)

/**
 * The wumpus is the monster of this game. He will eat the agent if they are on the same square.
 * 
 * @author Christopher McKee 
 * @version W13
 */
public class Wumpus extends Actor
{
    private GreenfootImage image;
    
    public Wumpus(int scale)
    {
        image = new GreenfootImage(getImage());
        image.scale(scale, scale);
        setImage(image);
    }
    /**
     * Act - do whatever the Wumpus wants to do. This method is called whenever
     * the 'Act' or 'Run' button gets pressed in the environment.
     */
    public void act() 
    {
        // Add code here if you want to wumpus to move.
    }    
}
