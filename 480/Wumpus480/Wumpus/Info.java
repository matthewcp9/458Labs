import greenfoot.*;  // (World, Actor, GreenfootImage, Greenfoot and MouseInfo)
import java.awt.Color;
import java.awt.Graphics;

/**
 * Score class to display points remaining points in the Wumpus world.
 * 
 * Adapted from Counter Support class created by Michael Kolling.
 * 
 * @author Chris McKee 
 * @version W2013
 */
public class Info extends Actor
{
    private static final Color textColor = java.awt.Color.BLACK;
    
    private int score;
    private String text;
    private int x, y;

    public Info()
    {
        this("", 1);
    }

    public Info(String prefix, int initScore)
    {
        text = prefix;
        score = initScore;
        
        setImage(new GreenfootImage(text + score, 32, Color.BLACK, Color.WHITE));
    }
    
    public void act() {
        updateImage();
    }

    public void add(int score)
    {
        this.score += score;
    }

    public void subtract(int score)
    {
        this.score -= score;
    }
    
    public void setScore(int score)
    {
        this.score = score;
    }

    public int getScore()
    {
        return score;
    }

    /**
     * Make the image
     */
    public void updateImage()
    {
        setImage(new GreenfootImage(text + score, 32, Color.BLACK, Color.WHITE));
    }    
}
