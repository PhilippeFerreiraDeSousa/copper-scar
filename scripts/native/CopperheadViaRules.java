import java.io.*;
import java.nio.file.*;
import java.util.*;
import app.freerouting.core.RoutingJob;
import app.freerouting.management.HeadlessBoardManager;
import app.freerouting.board.state.BoardObservers;
import app.freerouting.board.actions.ItemIdGenerator;
import app.freerouting.board.model.items.*;
import app.freerouting.board.model.structure.Component;
import app.freerouting.drc.ClearanceViolation;
import com.google.gson.GsonBuilder;

public class CopperheadViaRules { public static void main(String[] args)throws Exception {
  RoutingJob job=new RoutingJob();HeadlessBoardManager manager=new HeadlessBoardManager(job);
  BoardObservers observers=new BoardObservers(){public void notifyMoved(Component c){}public void notifyDeleted(Item x){}public void notifyChanged(Item x){}public void notifyNew(Item x){}public void activate(){}public void deactivate(){}public boolean isActive(){return false;}};
  var result=manager.loadFromSpecctraDsn(Files.newInputStream(Path.of(args[0])),observers,new ItemIdGenerator());
  var board=manager.getRoutingBoard();if(board==null)throw new RuntimeException("No loaded board: "+result);
List<Map<String,Object>> classes=new ArrayList<>();
for(int i=0;i<board.rules.netClasses.count();i++){var nc=board.rules.netClasses.get(i);List<String> viaNames=new ArrayList<>();var vr=nc.getViaRule();if(vr!=null)for(int v=0;v<vr.viaCount();v++)viaNames.add(vr.getVia(v).getPadstack().name);Map<String,Object> row=new LinkedHashMap<>();row.put("name",nc.getName());row.put("via_rule_padstacks",viaNames);classes.add(row);}
Map<String,Object> out=new LinkedHashMap<>();out.put("source",args[0]);out.put("routing_started",false);out.put("classes",classes);out.put("item_count",board.getItems().size());Files.writeString(Path.of(args[1]),new GsonBuilder().setPrettyPrinting().create().toJson(out));System.out.println(new GsonBuilder().create().toJson(out));
}}