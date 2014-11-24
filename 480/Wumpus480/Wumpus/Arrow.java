import greenfoot.*;  // (World, Actor, GreenfootImage, Greenfoot and MouseInfo)

/**
 * Write a description of class Arrow here.
 * 
 * @author (your name) 
 * @version (a version number or a date)
 */
public class Arrow extends Actor
{
    private GreenfootImage image;
    private String heading;
    private TheWumpusWorld world;
    public Arrow(TheWumpusWorld world, String direction)
    {
        this.world = world;
        image = new GreenfootImage(getImage());
        image.scale(world.getCellSize(), world.getCellSize());
        heading = direction;
        if(heading.equals("NORTH"))
            image.rotate(270);
        else if(heading.equals("EAST"))
            image.rotate(0);
        else if(heading.equals("SOUTH"))
            image.rotate(90);
        else if(heading.equals("WEST"))
            image.rotate(180);
        setImage(image);
    }
    /**
     * Act - do whatever the Arrow wants to do. This method is called whenever
     * the 'Act' or 'Run' button gets pressed in the environment.
     */
    public void act() 
    {
        moveForward();
    }    
    
    public void moveForward()
    {
        if(heading.equals("NORTH"))
        {
            if(getY() > 1)
                setLocation(getX(), getY() - 1);
            else
                (getWorld()).removeObject(this);
        }
        else if(heading.equals("EAST"))
        {
            if(getX() < world.getPlayWidth())
                setLocation(getX() + 1, getY());
            else
                (getWorld()).removeObject(this);
        }
        else if(heading.equals("SOUTH"))
        {
            if(getY() < world.getPlayWidth())
                setLocation(getX(), getY() + 1);
            else
                (getWorld()).removeObject(this);
        }
        else if(heading.equals("WEST"))
        {
            if(getX() > 1)
                setLocation(getX() - 1, getY());
            else
                (getWorld()).removeObject(this);
        }
    }
}
