import { useRouter } from "next/router";

import {
  DATA_DETECTION_ROUTE_DETAIL,
  DATA_DISCOVERY_ROUTE_DETAIL,
} from "~/features/common/nav/v2/routes";

const useDiscoveryRoutes = () => {
  const router = useRouter();
  const monitorId = router.query.monitorId as string;
  const currentResourceUrn = router.query.resourceUrn as string;

  const navigateToDetectionResults = ({
    resourceUrn,
    showFullSchema = false,
  }: {
    resourceUrn: string;
    showFullSchema?: boolean;
  }) => {
    router.push({
      pathname: DATA_DETECTION_ROUTE_DETAIL,
      query: {
        resourceUrn,
        showFullSchema,
      },
    });
  };

  const navigateToDiscoveryResults = ({
    resourceUrn,
  }: {
    resourceUrn: string;
  }) => {
    router.push({
      pathname: DATA_DISCOVERY_ROUTE_DETAIL,
      query: {
        resourceUrn,
      },
    });
  };

  return {
    monitorId,
    resourceUrn: currentResourceUrn,
    navigateToDetectionResults,
    navigateToDiscoveryResults,
  };
};
export default useDiscoveryRoutes;
