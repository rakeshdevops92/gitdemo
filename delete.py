def delete_old_files(currentdir, stpath, csvfile):
    """
    This method deletes files from the specified directory (stpath) if they meet the criteria.
    Criteria: 
    - Files with creation time older than 'csixyrsc' 
    - Files with modification time older than 'mtwoyrsc'
    
    Parameters:
    - currentdir: The current directory.
    - stpath: The directory path where the files are located.
    - csvfile: The path to the CSV file where the baseline data should be saved.
    """
    
    # Set up logging
    console = logging.StreamHandler()
    console.setLevel(logging.INFO)
    logging.basicConfig(level=logging.INFO, handlers=[console])

    setup_logger('log1', currentdir + '-old.txt')
    loggerOld = logging.getLogger('log1')
    
    setup_logger('log2', currentdir + '-current.txt')
    loggingCurrent = logging.getLogger('log2')
    
    setup_logger('log3', currentdir + '-error.txt')
    loggingError = logging.getLogger('log3')
    
    prfx = "\\\\UNC\\"
    stgpath = stpath + "/**/*"
    original_folder = Path(str(stgpath).replace('\\\\', prfx))

    files = glob.iglob(str(stgpath), recursive=True)
    
    # Variables to hold baseline data
    total_size_scanned = 0
    total_files_scanned = 0
    total_size_removed = 0
    total_files_removed = 0
    
    for filex in files:
        file = str(filex).replace('\\\\', prfx)
        
        if not os.path.isdir(file):
            extension = os.path.splitext(str(file))[1]
            try:
                file_size = os.path.getsize(str(file))
                total_size_scanned += file_size
                total_files_scanned += 1
                
                if os.stat(file).st_ctime < csixyrsc and os.stat(file).st_mtime < mtwoyrsc:
                    total_size_removed += file_size
                    total_files_removed += 1
                    
                    ext = extension
                    z = Path(file).name
                    sz = str(file_size)
                    on = io.owner(str(file))
                    cdt = str(datetime.fromtimestamp(os.stat(file).st_ctime))
                    mdt = str(datetime.fromtimestamp(os.stat(file).st_mtime))
                    adt = str(datetime.fromtimestamp(os.stat(file).st_atime))
                    er = ""

                    try:
                        os.remove(file)
                        loggingCurrent.info('%s|%s|%s|%s|%s|%s|Deleted', 
                                            sz, on, cdt, mdt, adt, str(file).replace("\\\\UNC\\", "\\"), er)
                    except Exception as e:
                        loggingError.info('%s|%s|%s|%s|%s|%s|%s|Error|%s', 
                                          sz, on, cdt, mdt, adt, str(file).replace("\\\\UNC\\", "\\"), er, str(e))
                        continue
            except OSError as ne:
                loggingError.info('%s|%s|%s|%s|%s|%s|%s|Error|%s', 
                                  "", "", "", "", "", str(file).replace("\\\\UNC\\", "\\"), "", str(ne))
                continue
    
    # Write baseline data to the CSV file
    with open(csvfile, mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["L Drive Retention Baseline"])
        writer.writerow(["Total size of files scanned", total_size_scanned])
        writer.writerow(["Total number of files scanned", total_files_scanned])
        writer.writerow(["Total size of files removed", total_size_removed])
        writer.writerow(["Total number of files removed", total_files_removed])

    loggingError.handlers.clear()
    loggerOld.handlers.clear()
    loggingCurrent.handlers.clear()
    logging.shutdown()
