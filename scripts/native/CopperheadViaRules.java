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
if(args.length>2){var expected=com.google.gson.JsonParser.parseString(Files.readString(Path.of(args[2]))).getAsJsonObject();var checks=new ArrayList<Map<String,Object>>();boolean all=true;
 for(var entry:expected.getAsJsonArray("targets")){var target=entry.getAsJsonObject();double x=target.getAsJsonArray("xy_dsn_um").get(0).getAsDouble(),y=target.getAsJsonArray("xy_dsn_um").get(1).getAsDouble();String net=target.get("net").getAsString();Via selected=null;int matches=0;
  for(var item:board.getItems())if(item instanceof Via via){var xy=board.communication.coordinateTransform.boardToDsn(via.getCenter().toFloat());if(Math.abs(xy[0]-x)<.001&&Math.abs(xy[1]-y)<.001&&via.netCount()==1&&board.rules.nets.get(via.getNetNumber(0)).name.equals(net)){selected=via;matches++;}}
  var actualPins=new TreeSet<String>();if(matches==1)for(var item:selected.getConnectedSet(selected.getNetNumber(0)))if(item instanceof Pin pin)actualPins.add(pin.componentName()+"."+pin.name());var expectedPins=new TreeSet<String>();for(var pin:target.getAsJsonArray("expected_pins"))expectedPins.add(pin.getAsString());boolean ok=matches==1&&actualPins.equals(expectedPins);all=all&&ok;checks.add(Map.of("net",net,"xy_dsn_um",List.of(x,y),"expected_pins",expectedPins,"actual_pins",actualPins,"ok",ok));
 }out.put("native_contact_checks",checks);out.put("native_contacts_match",all);Files.writeString(Path.of(args[1]),new GsonBuilder().setPrettyPrinting().create().toJson(out));
}
}}
