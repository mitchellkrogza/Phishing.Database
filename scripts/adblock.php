<?php
    /* Adblock Formatting Generator Script for the Phishing Database
     * Adapted from Script Copyright (c) 2017 Stevie-Ray - https://github.com/Stevie-Ray
     * Adapted by: Mitchell Krog (mitchellkrog@gmail.com) - https://github.com/mitchellkrogza
     * Repo Url: https://github.com/mitchellkrogza/Phishing.Database
     */
namespace mitchellkrogza;

use Mso\IdnaConvert\IdnaConvert;

class Generator
{
    
    private $projectUrl = "https://github.com/mitchellkrogza/Phishing.Database";
    public function generateFiles()
    {
        date_default_timezone_set('Africa/Johannesburg');
        $date = date('Y-m-d H:i:s');
        $lines = $this->domainWorker();
        $this->createNginx($lines);
    }


    /**
     * @return array
     */
    public function domainWorker()
    {
        $domainsFile = "./phishing-domains-ACTIVE.txt";

        $handle = fopen($domainsFile, "r");
        if (!$handle) {
            throw new \RuntimeException('Error opening file ' . $domainsFile);
        }
        $lines = array();
        while (($line = fgets($handle)) !== false) {
            $line = trim(preg_replace('/\s\s+/', ' ', $line));

            // convert internationalized domain names
            if (preg_match('/[А-Яа-яЁёɢ]/u', $line)) {

                $IDN = new IdnaConvert();

                $line = $IDN->encode($line);

            }

            if (empty($line)) {
                continue;
            }
            $lines[] = $line;
        }
        fclose($handle);
        $uniqueLines = array_unique($lines, SORT_STRING);
        sort($uniqueLines, SORT_STRING);
        if (is_writable($domainsFile)) {
            file_put_contents($domainsFile, implode("\n", $uniqueLines));
        } else {
            trigger_error("Permission denied");
        }

        return $lines;
    }

	/**
     * Write to File Function
     * @param $filename
     * @param $data
     */
    protected function writeToFile($filename, $data)
    {
    $file = "./active-domains.adblock";
	$handle = fopen($file, 'w') or die('Cannot open file:  '.$file);
	fwrite($handle, $data);
    }

    /**
     * @param string $date
     * @param array  $lines
     */
    public function createNginx(array $lines) 
    {
    $file = "./active-domains.adblock";
        $data = "";
    {
        foreach ($lines as $line) {
            $data .= "||" . preg_quote($line) . "^\n";
        }
        $this->writeToFile($file, $data);
    	}
	}
}
$generator = new Generator();
$generator->generateFiles();
