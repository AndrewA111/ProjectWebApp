import java.io.PrintStream;

public class Date {
	private int day;
	private int month;
	private int year;
	
	public Date(int d, int m, int y) {
		this.day = d;
		this.month = m;
		this.year = y;
	}
	
	/*
	 * Print date in format 'dd/mm/yyyy'
	 */
	public void print(PrintStream ps) {
		// check string.format format (why 0?)
		ps.print(String.format("%02d/%02d/%4d\n", this.day, this.month, this.year));
	}
	
	/*
	 * Method to return different in years between this date and a given date
	 * Difference taken as the difference between the two 'year' values for the date objects
	 */
	public int diffInYears(Date d) {
		return Math.abs(d.getYear() - this.year);
	}
	
	/*
	 * Getters
	 */
	public int getDay() {
		return day;
	}

	public int getMonth() {
		return month;
	}

	public int getYear() {
		return year;
	}
	
	
}