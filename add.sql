delete from DB.DBA.LOAD_LIST;
 commit work; 
 ld_add('/rdfData/rdfGraffiti.ttl','ingrid');
 rdf_loader_run();
 checkpoint;

delete from DB.DBA.LOAD_LIST;
 commit work; 
 ld_add('/rdfData/rdfCollections.ttl','ingrid');
 rdf_loader_run();
 checkpoint;

delete from DB.DBA.LOAD_LIST;
 commit work; 
 ld_add('/rdfData/rdfTags.ttl','ingrid');
 rdf_loader_run();
 checkpoint;

delete from DB.DBA.LOAD_LIST;
 commit work; 
 ld_add('/rdfData/crews_merged_v2.ttl','ingrid');
 rdf_loader_run();
 checkpoint;

delete from DB.DBA.LOAD_LIST;
 commit work; 
 ld_add('/rdfData/locationStreet_to_streets_lgd.nt','ingrid');
 rdf_loader_run();
 checkpoint;

delete from DB.DBA.LOAD_LIST;
 commit work; 
 ld_add('/rdfData/sameAsLinks.nt','ingrid');
 rdf_loader_run();
 checkpoint;

delete from DB.DBA.LOAD_LIST;
 commit work; 
 ld_add('/rdfData/sameAsLinksCityDbpedia.nt','ingrid');
 rdf_loader_run();
 checkpoint;
 exit;

delete from DB.DBA.LOAD_LIST;
 commit work; 
 ld_add('/rdfData/sameAsLinksCityLgdo.nt','ingrid');
 rdf_loader_run();
 checkpoint;
 exit;

delete from DB.DBA.LOAD_LIST;
 commit work; 
 ld_add('/rdfData/sameAs_sprayercrews_to_crewsInfo.nt','ingrid');
 rdf_loader_run();
 checkpoint;
 exit;

delete from DB.DBA.LOAD_LIST;
 commit work; 
 ld_add('/rdfData/symbols_v2.ttl','ingrid');
 rdf_loader_run();
 checkpoint;
 exit;