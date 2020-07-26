import static org.junit.Assert.*;

import org.junit.Test;


public class Tests {

	@TestDescription("Worker should have a boss once constucted.")
	@Test
	public void createdWorkerHasBoss() {
		Boss boss = new Boss("BossA", new Date(1,1,1980));
		Worker worker = new Worker("WorkerA", new Date(1,1,1990), boss);
		
		assertNotNull(worker.get_boss());
	}
	
	@TestDescription("Worker's boss should be the boss passed in the constuctor.")
	@Test
	public void createdWorkerHasCorrectBoss() {
		Boss boss = new Boss("BossA", new Date(1,1,1980));
		Worker worker = new Worker("WorkerA", new Date(1,1,1990), boss);
		
		assertEquals(boss.getName(), worker.get_boss().getName());
	}
	
	@TestDescription("Worker should be present in boss's list of workers.")
	@Test
	public void createdWorkerAddedToBoss() {
		Boss boss = new Boss("BossA", new Date(1,1,1980));
		Worker worker = new Worker("WorkerA", new Date(1,1,1990), boss);
		
		boolean workerFound = false;
		
		for(Person bossWorker : boss.getWorkers()) {
			if(bossWorker == (Person) worker) {
				workerFound = true;
			}
		}
		
		assertTrue(workerFound);
	}

}
