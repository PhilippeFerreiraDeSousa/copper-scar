import java.nio.file.*;
import java.util.*;
import app.freerouting.core.RoutingJob;
import app.freerouting.management.HeadlessBoardManager;
import app.freerouting.board.state.BoardObservers;
import app.freerouting.board.actions.ItemIdGenerator;
import app.freerouting.board.model.items.*;
import app.freerouting.board.model.structure.Component;
import app.freerouting.settings.RouterSettings;
import app.freerouting.settings.sources.DefaultSettings;
import app.freerouting.datastructures.Stoppable;
import app.freerouting.datastructures.TimeLimit;
import com.google.gson.GsonBuilder;

/** Bounded invocation of the stock engine fanout API; contains no path search. */
public class CopperheadFanout {
 public static void main(String[] args) throws Exception {
  var job=new RoutingJob();
  job.routerSettings=new DefaultSettings().getSettings();
  job.routerSettings.copperToEdgeClearanceUm=Double.parseDouble(args[3]);
  job.routerSettings.holeClearanceUm=Double.parseDouble(args[4]);
  var manager=new HeadlessBoardManager(job);
  BoardObservers observers=new BoardObservers(){public void notifyMoved(Component c){}public void notifyDeleted(Item x){}public void notifyChanged(Item x){}public void notifyNew(Item x){}public void activate(){}public void deactivate(){}public boolean isActive(){return false;}};
  try(var in=Files.newInputStream(Path.of(args[0]))){manager.loadFromSpecctraDsn(in,observers,new ItemIdGenerator());}
  var board=manager.getRoutingBoard();
  if(board==null)throw new IllegalStateException("DSN did not load");
  var settings=job.routerSettings;
  settings.setLayerCount(board.getLayerCount());
  settings.applyBoardSpecificOptimizations(board);
  settings.strictDrc=true; settings.automaticNeckdown=false;
  settings.fanout.enabled=true; settings.fanout.fallbackToBoardVias=false;
  settings.fanout.ripupAllowed=false;
  // Direct fanout uses existing board via rules. Keep displayed diameter settings
  // consistent as well; this wrapper never synthesizes a smaller via definition.
  settings.fanout.startViaDiameterMm=0.6; settings.fanout.endViaDiameterMm=0.6;
  var rows=new ArrayList<Map<String,Object>>();
  for(int i=5;i<args.length;i++){
   String target=args[i]; Pin selected=null;
   for(var item:board.getItems())if(item instanceof Pin pin && target.equals(pin.componentName()+"."+pin.name())){
    if(selected!=null)throw new IllegalArgumentException("Ambiguous pin "+target);selected=pin;
   }
   if(selected==null)throw new IllegalArgumentException("Missing pin "+target);
   var row=new LinkedHashMap<String,Object>();row.put("terminal",target);row.put("items_before",board.getItems().size());
   long start=System.nanoTime();
   Stoppable stopper=new Stoppable(){boolean stopped=false;public void requestStop(){stopped=true;}public boolean isStopRequested(){return stopped;}};
   var result=board.fanout(selected,settings,-1,stopper,new TimeLimit(30000));
   row.put("state",result.state.toString());row.put("details",result.details);row.put("elapsed_seconds",(System.nanoTime()-start)/1e9);row.put("items_after",board.getItems().size());rows.add(row);
   System.out.println(new GsonBuilder().create().toJson(row));
  }
  try(var out=Files.newOutputStream(Path.of(args[1]))){if(!manager.saveAsSpecctraSessionSes(out,"pcbgolf"))throw new IllegalStateException("SES export failed");}
  var report=new LinkedHashMap<String,Object>();report.put("engine_operation","RoutingBoard.fanout");report.put("ripup_allowed",false);report.put("via_rules","existing DSN definitions only");report.put("automatic_neckdown",false);report.put("strict_drc_configured",true);report.put("acceptance","independent native after_fanout gate required");report.put("settings",settings);report.put("per_terminal_seconds",30);report.put("terminals",rows);
  Files.writeString(Path.of(args[2]),new GsonBuilder().setPrettyPrinting().create().toJson(report));
 }
}
