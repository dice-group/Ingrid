package ingrid.dice_research;

import java.io.File;
import java.io.FileWriter;
import java.io.IOException;
import java.util.HashSet;
import java.util.Set;

import org.apache.jena.datatypes.xsd.XSDDatatype;
import org.apache.jena.query.QueryExecution;
import org.apache.jena.query.QueryExecutionFactory;
import org.apache.jena.query.QuerySolution;
import org.apache.jena.query.ResultSet;
import org.apache.jena.rdf.model.Literal;
import org.apache.jena.rdf.model.Model;
import org.apache.jena.rdf.model.ModelFactory;
import org.apache.jena.rdf.model.Property;
import org.apache.jena.rdf.model.Resource;
import org.apache.jena.rdf.model.ResourceFactory;

/**
 * Generates the public version of the Knowledge Graph from the private graph.
 * 
 * @author Alexandra Silva
 *
 */
public class PrivateFilterMain {
	private static final Resource TAG_8 = ResourceFactory
			.createResource("https://graffiti.data.dice-research.org/resource/tag_8");
	private static final Property HAS_TAG = ResourceFactory
			.createProperty("https://graffiti.data.dice-research.org/graffiti/hasTagId");
	private static final Property IN_INVENTORY = ResourceFactory
			.createProperty("https://graffiti.data.dice-research.org/graffiti/inInventory");
	private static final Literal KREUZER = ResourceFactory.createTypedLiteral("Stadtarchiv München, Sammlung Kreuzer",
			XSDDatatype.XSDstring);
	private static final Property HAS_URI = ResourceFactory
			.createProperty("https://graffiti.data.dice-research.org/graffiti/hasUri");

	private static final Property NOTE = ResourceFactory
			.createProperty("https://graffiti.data.dice-research.org/graffiti/hasNote");
	private static final Property REDAKTEUR = ResourceFactory
			.createProperty("https://graffiti.data.dice-research.org/graffiti/hasEditor");
	private static final Property BEARBEITNGSTAND = ResourceFactory
			.createProperty("https://graffiti.data.dice-research.org/graffiti/hasProcessingStatus");
	private static final Property ID = ResourceFactory
			.createProperty("https://graffiti.data.dice-research.org/graffiti/hasId");
	private static final Property LAST_MOD = ResourceFactory
			.createProperty("https://graffiti.data.dice-research.org/graffiti/hasOriginalFile");
	private static final Property ORIG_FOTO = ResourceFactory
			.createProperty("https://graffiti.data.dice-research.org/graffiti/hasOriginalfoto");
	private static final Property PROC_DATE = ResourceFactory
			.createProperty("https://graffiti.data.dice-research.org/graffiti/hasProcessingDate");

	private static final Property ANNOTATOR = ResourceFactory
			.createProperty("https://graffiti.data.dice-research.org/graffiti/hasAnnotator");

	private static final Property SIXOMCID = ResourceFactory
			.createProperty("https://graffiti.data.dice-research.org/graffiti/hasSixomcid");

	private static final Property SIXOMCUID = ResourceFactory
			.createProperty("https://graffiti.data.dice-research.org/graffiti/hasSixomcuid");

	private static final Property FUNDORT = ResourceFactory
			.createProperty("https://graffiti.data.dice-research.org/graffiti/hasFundortGPS");

	private static final Property UUID = ResourceFactory
			.createProperty("https://graffiti.data.dice-research.org/graffiti/hasUuid");

	public static void main(String[] args) {
		Model model = ModelFactory.createDefaultModel();
		File folder = new File("rdf");
		for (File file : folder.listFiles()) {
			model.read(file.getAbsolutePath());
		}
		System.out.println("Initial size: " + model.size());

		// Filter properties
		System.out.println("Filtering properties");
		model.removeAll(null, NOTE, null);
		model.removeAll(null, REDAKTEUR, null);
		model.removeAll(null, ANNOTATOR, null);
		model.removeAll(null, BEARBEITNGSTAND, null);
		model.removeAll(null, ID, null);
		model.removeAll(null, LAST_MOD, null);
		model.removeAll(null, ORIG_FOTO, null);
		model.removeAll(null, PROC_DATE, null);
		model.removeAll(null, SIXOMCID, null);
		model.removeAll(null, SIXOMCUID, null);
		model.removeAll(null, FUNDORT, null);
		model.removeAll(null, UUID, null);

		System.out.println("Filtering properties done");
		System.out.println(model.size());

		// Filter graffiti by the tag "Freigabe Recherche"
		System.out.println("Filtering tags and inventory");
		String allQuery = "select distinct ?i where { ?i a <https://graffiti.data.dice-research.org/ontology/Graffiti> .}";
		Set<Resource> allGraffiti = executeSelectQuery(model, allQuery);
		for (Resource curRes : allGraffiti) {
			boolean hasTag8 = model.listStatements(curRes, HAS_TAG, TAG_8).hasNext();
			if (!hasTag8) {
				model.removeAll(curRes, null, null);
			}

			// Filter images unless Kreuzer :inInventory

			boolean isKreuzer = model.listStatements(curRes, IN_INVENTORY, KREUZER).hasNext();
			if (!isKreuzer) {
				model.removeAll(curRes, HAS_URI, null);

				removeExtraImgFiles(model, curRes);
			}
		}
		System.out.println("Final size: " + model.size());

		try (FileWriter out = new FileWriter("public_rdfGraffiti.ttl");) {
			model.write(out, "TTL");
		} catch (IOException e) {
			e.printStackTrace();
		}
	}

	/**
	 * Removes all the Image Files connected to a resource.
	 * 
	 * @param model
	 * @param curRes
	 */
	private static void removeExtraImgFiles(Model model, Resource curRes) {
		StringBuilder queryBuilder = new StringBuilder();
		queryBuilder.append("select distinct ?i where { <");
		queryBuilder.append(curRes.getURI()).append("> ?p ?i . ");
		queryBuilder.append("?i a <https://graffiti.data.dice-research.org/ontology/ImageFile> . }");
		Set<Resource> fileImages = executeSelectQuery(model, queryBuilder.toString());
		for (Resource curImage : fileImages) {
			model.removeAll(curImage, HAS_URI, null);
		}
	}

	/**
	 * Executes a select SPARQL query over a Jena Model and returns the set of
	 * resources.
	 * 
	 * @param model The Jena model.
	 * @param query The query string.
	 * @return
	 */
	private static Set<Resource> executeSelectQuery(Model model, String query) {
		Set<Resource> resSet = new HashSet<Resource>();
		try (QueryExecution qe = QueryExecutionFactory.create(query, model)) {
			ResultSet result = qe.execSelect();
			while (result.hasNext()) {
				QuerySolution qs = result.nextSolution();
				resSet.add(qs.getResource("i"));
			}
		} catch (Exception e) {
			e.printStackTrace();
		}
		return resSet;
	}
}
