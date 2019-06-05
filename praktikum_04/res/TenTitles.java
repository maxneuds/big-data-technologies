
import java.io.IOException;
import java.util.Iterator;
import java.util.logging.Level;
import java.util.logging.Logger;
import org.apache.hadoop.conf.Configuration;
import org.apache.hadoop.conf.Configured;
import org.apache.hadoop.fs.Path;
import org.apache.hadoop.io.IntWritable;
import org.apache.hadoop.io.Text;
import org.apache.hadoop.mapreduce.Job;
import org.apache.hadoop.mapreduce.Mapper;
import org.apache.hadoop.mapreduce.Reducer;
import org.apache.hadoop.mapreduce.lib.input.FileInputFormat;
import org.apache.hadoop.mapreduce.lib.output.FileOutputFormat;
import org.apache.hadoop.mapreduce.lib.output.TextOutputFormat;
import org.apache.hadoop.util.Tool;
import org.apache.hadoop.util.ToolRunner;
import org.json.simple.JSONArray;
import org.json.simple.JSONObject;
import org.json.simple.parser.JSONParser;
import org.json.simple.parser.ParseException;

public class TenTitles extends Configured implements Tool {
    public static class MoviesMapper extends Mapper<Object, Text, Text, Text> {
        private Text word = new Text();
		private Text word2 = new Text();
        public void map(Object key, Text value, Context context) throws IOException, InterruptedException {
            try {
                JSONParser jsonParser = new JSONParser();
                JSONObject movieObject = (JSONObject) jsonParser.parse(value.toString());
                JSONArray ratingsArrayObject = (JSONArray) movieObject.get("ratings");
                Iterator i = ratingsArrayObject.iterator();
				boolean ten = false;
                while (i.hasNext()) {
                    JSONObject ratingsObject = (JSONObject) i.next();
                    if ((Long) ratingsObject.get("userId") == 10) {
						ten = true;
					}
					
                }

				if (ten) {
					word.set("Title");
					word2.set((String) movieObject.get("title"));
					context.write(word, word2);
				}
                
            } catch (ParseException ex) {
                Logger.getLogger(TenTitles.class.getName()).log(Level.SEVERE, null, ex);
            }
        }
    }

    public static class TitlesReducer extends Reducer<Text, Text, Text, Text> {
		private Text word = new Text();
        public void reduce(Text key, Iterable<Text> values, Context context) throws IOException, InterruptedException {
			String titles = "";
            for (Text val : values) {
                titles += val + ", ";
            }
            word.set(titles);
			
            context.write(key, word);
        }
    }

    public static void main(String[] args) throws Exception {
        int exitCode = ToolRunner.run(new TenTitles(), args);
        System.exit(exitCode);
    }

    public int run(String[] args) throws Exception {
        if (args.length != 2) {
            System.err.printf("Usage: %s needs two arguments, input and output files\n", getClass().getSimpleName());
            return -1;
        }

		// when implementing tool
        Configuration conf = this.getConf();
        
		// create job
		Job job = Job.getInstance(conf, "TenTitles");
        job.setJarByClass(TenTitles.class);
        
		// set the input and output path
		FileInputFormat.addInputPath(job, new Path(args[0]));
        FileOutputFormat.setOutputPath(job, new Path(args[1]));
        
		// set the key and value class
		job.setOutputKeyClass(Text.class);
        job.setOutputValueClass(Text.class);
        job.setOutputFormatClass(TextOutputFormat.class);
		
		// set the mapper and reducer class
        job.setMapperClass(MoviesMapper.class);
        job.setReducerClass(TitlesReducer.class);
		

		// wait for the job to finish
        int returnValue = job.waitForCompletion(true) ? 0 : 1;
		
	    // monitor & output execution time
        if (job.isSuccessful()) {
            System.out.println("Job was successful");
            System.out.println("Time: " + String.valueOf(job.getStartTime() - job.getFinishTime()));
        } else if (!job.isSuccessful()) {
            System.out.println("Job was not successful");
        }
        return returnValue;
    }

    
}
