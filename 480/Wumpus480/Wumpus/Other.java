import greenfoot.*;  // (World, Actor, GreenfootImage, Greenfoot and MouseInfo)

/**
 * Write a description of class Other here.
 * 
 * @author (your name) 
 * @version (a version number or a date)
 */
public class Other extends Actor
{
    private static GreenfootImage breeze = new GreenfootImage("Breeze.png");
    private static GreenfootImage cell = new GreenfootImage("Cell.png");
    private static GreenfootImage pit = new GreenfootImage("Pit.png");
    private static GreenfootImage stench = new GreenfootImage("Stench.png");
    private static GreenfootImage wall = new GreenfootImage("Brick.jpg");
    
    public Other(int scale, String str)
    {
        breeze.scale(scale, scale);
        cell.scale(scale, scale);
        pit.scale(scale, scale);
        stench.scale(scale, scale);
        wall.scale(scale, scale);
        if(str.equals("breeze"))
            setImage(breeze);
        else if(str.equals("cell"))
            setImage(cell);
        else if(str.equals("pit"))
            setImage(pit);
        else if(str.equals("stench"))
            setImage(stench);
        else if(str.equals("wall"))
            setImage(wall);
        else
            setImage(new GreenfootImage(scale, scale));
    }
    
    /**
     * Act - do whatever the Other wants to do. This method is called whenever
     * the 'Act' or 'Run' button gets pressed in the environment.
     */
    public void act() 
    {
        // Do nothing
    }    
}
